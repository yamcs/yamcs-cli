from yamcs.cli import utils
from yamcs.cli.completers import SpaceSystemCompleter
from yamcs.client import YamcsClient


class SpaceSystemsCommand(utils.Command):
    def __init__(self, parent):
        super(SpaceSystemsCommand, self).__init__(
            parent, "space-systems", "Read space systems"
        )

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List space systems")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(
            subparsers, "describe", "Describe a space system"
        )
        subparser.add_argument(
            "space_system", metavar="NAME", type=str, help="name of the space system"
        ).completer = SpaceSystemCompleter
        subparser.set_defaults(func=self.describe)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())

        rows = [["NAME", "DESCRIPTION"]]
        for space_system in mdb.list_space_systems():
            rows.append(
                [
                    space_system.qualified_name,
                    space_system.description,
                ]
            )
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        space_system = mdb.get_space_system(args.space_system)
        print(space_system._proto)
