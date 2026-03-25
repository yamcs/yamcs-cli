import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Container, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ContainerCompleter


class ContainersCommand(utils.Command):
    def __init__(self, parent):
        super(ContainersCommand, self).__init__(parent, "containers", "Read containers")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List containers")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
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
        iterator = mdb.list_containers()
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Container]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Container]):
        rows: List[List[Any]] = [["NAME", "DESCRIPTION"]]
        for container in iterator:
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
