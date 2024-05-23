import binascii
import sys
from itertools import islice
from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils


class PacketsCommand(utils.Command):
    def __init__(self, parent):
        super(PacketsCommand, self).__init__(parent, "packets", "Read packets")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "log", "Read packet log")
        subparser.add_argument(
            "-p",
            "--packet",
            type=str,
            help="Filter by packet name",
        )
        subparser.add_argument(
            "-n",
            "--lines",
            type=str,
            default=10,
            help="Number of packets to show",
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include packets not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include packets not newer than the specified date",
        )
        subparser.set_defaults(func=self.log)

        subparser = self.create_subparser(
            subparsers, "rebuild-histogram", "Rebuild packet histogram"
        )
        subparser.set_defaults(func=self.rebuild_histogram)
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include packets not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include packets not newer than the specified date",
        )

        subparser = self.create_subparser(
            subparsers, "rebuild-ccsds-index", "Rebuild CCSDS index"
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include packets not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include packets not newer than the specified date",
        )
        subparser.set_defaults(func=self.rebuild_ccsds_index)

    def log(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = None
        if args.since:
            start = utils.parse_timestamp(args.since)
        stop = None
        if args.until:
            stop = utils.parse_timestamp(args.until)

        most_recent_only = start is None and stop is None and args.lines != "all"

        iterator = archive.list_packets(
            name=args.packet,
            descending=most_recent_only,
            start=start,
            stop=stop,
        )

        # Limit, unless explicit filters are set
        # We need to reverse it back to ascending in-memory.
        if most_recent_only:
            iterator = reversed(list(islice(iterator, 0, int(args.lines))))

        rows: List[List[Any]] = [["NAME", "TIME", "DATA"]]
        for packet in iterator:
            row = [
                packet.name,
                packet.generation_time,
                str(binascii.hexlify(packet.binary), "ascii"),
            ]
            rows.append(row)
        utils.print_table(rows)

    def rebuild_histogram(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())
        start = None
        if args.since:
            start = utils.parse_timestamp(args.since)
        stop = None
        if args.until:
            stop = utils.parse_timestamp(args.until)

        sys.stderr.write("Rebuilding packet histogram")
        sys.stderr.flush()
        archive.rebuild_histogram("tm", start=start, stop=stop)
        sys.stderr.write("done\n")
        sys.stderr.flush()

    def rebuild_ccsds_index(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = None
        if args.since:
            start = utils.parse_timestamp(args.since)
        stop = None
        if args.until:
            stop = utils.parse_timestamp(args.until)

        sys.stderr.write("Rebuilding CCSDS index... ")
        sys.stderr.flush()
        archive.rebuild_ccsds_index(start, stop)
        sys.stderr.write("done\n")
        sys.stderr.flush()
