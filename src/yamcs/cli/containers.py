from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ContainerCompleter


class ContainersCommand(utils.Command):
    def __init__(self, parent):
        super(ContainersCommand, self).__init__(parent, "containers", "Read containers")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List containers")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(
            subparsers, "describe", "Describe a container"
        )
        subparser.add_argument(
            "container", metavar="NAME", type=str, help="name of the container"
        ).completer = ContainerCompleter
        subparser.set_defaults(func=self.describe)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())

        rows: List[List[Any]] = [["NAME", "DESCRIPTION"]]
        for container in mdb.list_containers():
            rows.append(
                [
                    container.qualified_name,
                    container.description,
                ]
            )
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        container = mdb.get_container(args.container)
        print(container._proto)
