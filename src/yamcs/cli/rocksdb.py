import sys
from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils


class RocksDBCommand(utils.Command):
    def __init__(self, parent):
        super(RocksDBCommand, self).__init__(
            parent, "rocksdb", "Manage RocksDB storage engine"
        )

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "tablespaces", "List tablespaces")
        subparser.set_defaults(func=self.tablespaces)

        subparser = self.create_subparser(
            subparsers, "compact", "Compact column family"
        )
        subparser.set_defaults(func=self.compact)
        subparser.add_argument(
            "tablespace",
            metavar="TABLESPACE",
            type=str,
            help="RocksDB tablespace",
        )
        subparser.add_argument(
            "cf",
            metavar="CF",
            type=str,
            help="RocksDB column family",
        )
        subparser.add_argument(
            "--dbpath",
            metavar="PATH",
            type=str,
            help="Path within the tablespace",
        )

    def tablespaces(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        rows: List[List[Any]] = [["NAME", "DATA DIR"]]
        for tablespace in client.list_rdb_tablespaces():
            rows.append([tablespace.name, tablespace.data_dir])
        utils.print_table(rows)

    def compact(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        sys.stderr.write("Compacting... ")
        sys.stderr.flush()
        client.compact_rdb_column_family(
            tablespace=args.tablespace,
            cf=args.cf,
            dbpath=args.dbpath or "",
        )
        sys.stderr.write("done\n")
        sys.stderr.flush()
