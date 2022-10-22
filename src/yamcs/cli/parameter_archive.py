from yamcs.cli import utils
from yamcs.client import YamcsClient


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

    def rebuild(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = utils.parse_timestamp(args.start)
        stop = utils.parse_timestamp(args.stop)

        archive.rebuild_parameter_archive(start=start, stop=stop)
        print("Task submitted. It will finish asynchronously.")
