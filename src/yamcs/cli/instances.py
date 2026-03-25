import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Instance, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import InstanceCompleter


class InstancesCommand(utils.Command):
    def __init__(self, parent):
        super(InstancesCommand, self).__init__(parent, "instances", "Read instances")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List instances")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "start", "Start an instance")
        subparser.add_argument(
            "instances",
            metavar="INSTANCE",
            type=str,
            nargs="+",
            help="name of the instance",
        ).completer = InstanceCompleter
        subparser.set_defaults(func=self.start)

        subparser = self.create_subparser(subparsers, "stop", "Stop an instance")
        subparser.add_argument(
            "instances",
            metavar="INSTANCE",
            type=str,
            nargs="+",
            help="name of the instance",
        ).completer = InstanceCompleter
        subparser.set_defaults(func=self.stop)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        iterator = client.list_instances()
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Instance]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Instance]):
        rows: List[List[Any]] = [["NAME", "STATE", "MISSION TIME"]]
        for instance in iterator:
            rows.append(
                [
                    instance.name,
                    instance.state,
                    instance.mission_time,
                ]
            )
        utils.print_table(rows)

    def start(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for instance in args.instances:
            client.start_instance(instance)

    def stop(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for instance in args.instances:
            client.stop_instance(instance)
