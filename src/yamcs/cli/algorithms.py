from yamcs.cli import utils
from yamcs.cli.completers import AlgorithmCompleter
from yamcs.client import YamcsClient


class AlgorithmsCommand(utils.Command):
    def __init__(self, parent):
        super(AlgorithmsCommand, self).__init__(parent, "algorithms", "Read algorithms")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List algorithms")
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

        rows = [["NAME", "DESCRIPTION"]]
        for algorithm in mdb.list_algorithms():
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
