import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Service, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ServiceCompleter


class ServicesCommand(utils.Command):
    def __init__(self, parent):
        super(ServicesCommand, self).__init__(parent, "services", "Manage services")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List services")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "start", "Start a service")
        subparser.add_argument(
            "services",
            metavar="SERVICE",
            type=str,
            nargs="+",
            help="name of the service",
        ).completer = ServiceCompleter
        subparser.set_defaults(func=self.start)

        subparser = self.create_subparser(subparsers, "stop", "Stop a service")
        subparser.add_argument(
            "services",
            metavar="SERVICE",
            type=str,
            nargs="+",
            help="name of the service",
        ).completer = ServiceCompleter
        subparser.set_defaults(func=self.stop)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        iterator = client.list_services(opts.require_instance())
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Service]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Service]):
        rows: List[List[Any]] = [["NAME", "CLASS", "STATUS"]]
        for service in iterator:
            rows.append(
                [
                    service.name,
                    service.class_name,
                    service.state,
                ]
            )
        utils.print_table(rows)

    def start(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for service in args.services:
            client.start_service(opts.require_instance(), service=service)

    def stop(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for service in args.services:
            client.stop_service(opts.require_instance(), service=service)
