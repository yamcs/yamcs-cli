from yamcs.cli import utils
from yamcs.cli.completers import ParameterCompleter
from yamcs.client import YamcsClient


class ParametersCommand(utils.Command):
    def __init__(self, parent):
        super(ParametersCommand, self).__init__(parent, "parameters", "Read parameters")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List parameters")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(
            subparsers, "describe", "Describe a parameter"
        )
        subparser.add_argument(
            "parameter", metavar="NAME", type=str, help="name of the parameter"
        ).completer = ParameterCompleter
        subparser.set_defaults(func=self.describe)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())

        rows = [["NAME", "DATA SOURCE"]]
        for parameter in mdb.list_parameters():
            rows.append(
                [
                    parameter.qualified_name,
                    parameter.data_source,
                ]
            )
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        parameter = mdb.get_parameter(args.parameter)
        print(parameter._proto)
