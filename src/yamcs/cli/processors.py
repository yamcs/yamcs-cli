import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Processor, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ProcessorCompleter


class ProcessorsCommand(utils.Command):
    def __init__(self, parent):
        super(ProcessorsCommand, self).__init__(parent, "processors", "Read processors")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List processors")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "delete", "Delete processor")
        subparser.add_argument(
            "processors",
            metavar="PROCESSOR",
            type=str,
            nargs="+",
            help="name of the processor",
        ).completer = ProcessorCompleter
        subparser.set_defaults(func=self.delete)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        iterator = client.list_processors(opts.require_instance())
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Processor]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Processor]):
        rows: List[List[Any]] = [
            [
                "NAME",
                "TYPE",
                "OWNER",
                "PERSISTENT",
                "PROTECTED",
                "MISSION TIME",
                "STATE",
            ]
        ]
        for processor in iterator:
            rows.append(
                [
                    processor.name,
                    processor.type,
                    processor.owner,
                    processor.persistent,
                    processor.protected,
                    processor.mission_time,
                    processor.state,
                ]
            )
        utils.print_table(rows)

    def delete(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        for processor in args.processors:
            client.delete_processor(opts.require_instance(), processor)
