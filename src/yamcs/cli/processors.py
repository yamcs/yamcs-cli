from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ProcessorCompleter


class ProcessorsCommand(utils.Command):
    def __init__(self, parent):
        super(ProcessorsCommand, self).__init__(parent, "processors", "Read processors")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List processors")
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
        for processor in client.list_processors(opts.require_instance()):
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
