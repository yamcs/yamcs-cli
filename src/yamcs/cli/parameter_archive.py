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
            help="Start time",
        )
        subparser.add_argument(
            "stop",
            metavar="STOP",
            type=str,
            help="Stop time",
        )
        subparser = self.create_subparser(
            subparsers, "purge", "Remove all data from the Parameter Archive"
        )
        subparser.set_defaults(func=self.purge)

    def rebuild(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = utils.parse_timestamp(args.start)
        stop = utils.parse_timestamp(args.stop)

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
