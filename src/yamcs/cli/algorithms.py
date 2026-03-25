import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Algorithm, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import AlgorithmCompleter


class AlgorithmsCommand(utils.Command):
    def __init__(self, parent):
        super(AlgorithmsCommand, self).__init__(parent, "algorithms", "Read algorithms")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List algorithms")
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
            subparsers, "describe", "Describe an algorithm"
        )
        subparser.add_argument(
            "algorithm", metavar="NAME", type=str, help="name of the algorithm"
        ).completer = AlgorithmCompleter
        subparser.set_defaults(func=self.describe)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        iterator = mdb.list_algorithms()
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Algorithm]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Algorithm]):
        rows: List[List[Any]] = [["NAME", "DESCRIPTION"]]
        for algorithm in iterator:
            rows.append(
                [
                    algorithm.qualified_name,
                    algorithm.description,
                ]
            )
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        algorithm = mdb.get_algorithm(args.algorithm)
        print(algorithm._proto)
