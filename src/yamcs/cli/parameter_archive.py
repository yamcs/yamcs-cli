import argparse
import sys

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.utils import eprint


class ParameterArchiveCommand(utils.Command):
    def __init__(self, parent):
        super(ParameterArchiveCommand, self).__init__(
            parent, "parameter-archive", "Manipulate the Parameter Archive"
        )

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(
            subparsers, "rebuild", "Rebuild the Parameter Archive"
        )
        subparser.set_defaults(func=self.rebuild)
        subparser.add_argument(
            "start",
            metavar="START",
            type=str,
            help=argparse.SUPPRESS,  # Deprecated
            nargs="?",
        )
        subparser.add_argument(
            "stop",
            metavar="STOP",
            type=str,
            help=argparse.SUPPRESS,  # Deprecated
            nargs="?",
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Ignore data before the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Ignore data after the specified date",
        )
        subparser = self.create_subparser(
            subparsers, "purge", "Remove all data from the Parameter Archive"
        )
        subparser.set_defaults(func=self.purge)
        subparser = self.create_subparser(
            subparsers, "backfilling", "Manage Parameter Archive backfilling"
        )
        subparser.add_argument(
            "action",
            metavar="ACTION",
            type=str,
            choices=["enable", "disable"],
            help="either enable or disable",
        )
        subparser.set_defaults(func=self.backfilling)

    def rebuild(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = None
        if args.start:
            eprint(
                "*** WARNING: deprecated use of positional 'START' argument. "
                "Use --since START instead."
            )
            start = utils.parse_timestamp(args.start)
        elif args.since:
            start = utils.parse_timestamp(args.since)

        stop = None
        if args.stop:
            eprint(
                "*** WARNING: deprecated use of positional 'STOP' argument. "
                "Use --until STOP instead."
            )
            stop = utils.parse_timestamp(args.stop)
        elif args.until:
            stop = utils.parse_timestamp(args.until)

        archive.rebuild_parameter_archive(start=start, stop=stop)
        eprint("Task submitted. It will finish asynchronously.")

    def purge(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        sys.stderr.write("Purging Parameter Archive... ")
        sys.stderr.flush()
        archive.purge_parameter_archive()
        sys.stderr.write("done\n")
        sys.stderr.flush()

    def backfilling(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        if args.action.lower() == "enable":
            sys.stderr.write("Enabling automatic backfilling... ")
            sys.stderr.flush()
            archive.enable_parameter_archive_backfilling()
            sys.stderr.write("done\n")
            sys.stderr.flush()
        elif args.action.lower() == "disable":
            sys.stderr.write("Disabling automatic backfilling... ")
            sys.stderr.flush()
            archive.disable_parameter_archive_backfilling()
            sys.stderr.write("done\n")
            sys.stderr.flush()
