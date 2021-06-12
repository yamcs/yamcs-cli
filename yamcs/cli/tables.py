import gzip
import os
import time
from sys import stdout

from yamcs.cli import utils
from yamcs.client import YamcsClient


class TablesCommand(utils.Command):
    def __init__(self, parent):
        super(TablesCommand, self).__init__(
            parent, "tables", "Read and manipulate tables"
        )

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List tables")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "describe", "Describe a table")
        subparser.add_argument(
            "table", metavar="TABLE", type=str, help="name of the table"
        )
        subparser.set_defaults(func=self.describe)

        subparser = self.create_subparser(subparsers, "dump", "Dump tables")
        subparser.add_argument(
            "tables", metavar="TABLE", type=str, nargs="+", help="name of the tables"
        )
        subparser.set_defaults(func=self.dump)
        subparser.add_argument(
            "-d",
            "--dir",
            type=str,
            help=(
                "Specifies the directory where to output dump files. "
                "Defaults to current directory"
            ),
        )
        subparser.add_argument(
            "--gzip", dest="gzip", action="store_true", help="Compress the output"
        )

        subparser = self.create_subparser(subparsers, "load", "Load tables")
        subparser.add_argument(
            "tables", metavar="TABLE", type=str, nargs="+", help="name of the tables"
        )
        subparser.set_defaults(func=self.load)
        subparser.add_argument(
            "-d",
            "--dir",
            type=str,
            help=(
                "Specifies the directory where to locate dump files. "
                "Defaults to current directory"
            ),
        )
        subparser.add_argument(
            "--gzip", dest="gzip", action="store_true", help="Decompress the input"
        )

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.instance)

        rows = [["NAME"]]
        for table in archive.list_tables():
            rows.append([table.name])
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.instance)
        table = archive.get_table(args.table)
        print(table._proto)

    def dump(self, args):
        if args.dir:
            if not os.path.exists(args.dir):
                os.makedirs(args.dir)

        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.instance)
        for table in args.tables:
            path = table + ".dump.gz" if args.gzip else table + ".dump"
            if args.dir:
                path = os.path.join(args.dir, path)
            if args.gzip:
                with gzip.open(path, "wb", compresslevel=1) as f:
                    self.write_dump(f, archive, table, path)
            else:
                with open(path, "wb") as f:
                    self.write_dump(f, archive, table, path)

    def write_dump(self, f, archive, table, path):
        txsize = 0
        t0 = time.time()
        t = t0
        prev_t = None
        for chunk in archive.dump_table(table):
            txsize += f.write(chunk)
            t = time.time()
            if not prev_t or (t - prev_t > 0.5):  # Limit console writes
                self.report_dump_stats(path, txsize, t - t0)
                prev_t = t
        if txsize > 0:
            self.report_dump_stats(path, txsize, t - t0)
            stdout.write("\n")

    def report_dump_stats(self, path, txsize, elapsed):
        fsize = os.path.getsize(path)
        rate = (txsize / 1024 / 1024) / elapsed
        stdout.write(
            "\r{}: {:.2f} MB (rx: {:.2f} MB at {:.2f} MB/s)".format(
                path, fsize / 1024 / 1024, txsize / 1024 / 1024, rate
            )
        )
        stdout.flush()

    def load(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.instance)
        for table in args.tables:
            path = table + ".dump.gz" if args.gzip else table + ".dump"
            if args.dir:
                path = os.path.join(args.dir, path)
            if args.gzip:
                with gzip.open(path, "rb") as f:
                    self.read_dump(f, archive, table, path)
            else:
                with open(path, "rb") as f:
                    self.read_dump(f, archive, table, path)

    def read_dump(self, f, archive, table, path):
        txsize = 0
        t0 = time.time()
        t = t0
        prev_t = None
        chunk_size = 32 * 1024
        fsize = os.path.getsize(path)

        def report_load_stats(elapsed):
            nonlocal path, fsize, txsize
            rate = (txsize / 1024 / 1024) / elapsed
            stdout.write(
                "\r{}: {:.2f} MB (rx: {:.2f} MB at {:.2f} MB/s)".format(
                    path, fsize / 1024 / 1024, txsize / 1024 / 1024, rate
                )
            )
            stdout.flush()

        def read_in_chunks():
            nonlocal f, txsize, t0, t, prev_t
            chunk = f.read(chunk_size)
            while chunk:
                yield chunk
                txsize += len(chunk)
                t = time.time()
                if not prev_t or (t - prev_t > 0.5):  # Limit console writes
                    report_load_stats(t - t0)
                    prev_t = t
                chunk = f.read(chunk_size)
            if txsize > 0:
                report_load_stats(t - t0)
                stdout.write("\n")

        archive.load_table(table, data=read_in_chunks(), chunk_size=None)
