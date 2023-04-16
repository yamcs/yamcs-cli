import binascii

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ParameterCompleter, ProcessorCompleter


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
            "parameter", metavar="PARAMETER", type=str, help="name of the parameter"
        ).completer = ParameterCompleter
        subparser.set_defaults(func=self.describe)

        subparser = self.create_subparser(subparsers, "get", "Get a parameter's value")
        subparser.add_argument(
            "parameter", metavar="PARAMETER", type=str, help="name of the parameter"
        ).completer = ParameterCompleter
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument(
            "--next", dest="next", action="store_true", help="Wait for the next value"
        )
        subparser.add_argument(
            "--timeout",
            dest="timeout",
            default=10,
            type=float,
            help="Timeout in seconds when using the --next option",
        )
        subparser.set_defaults(func=self.get)

        subparser = self.create_subparser(subparsers, "set", "Set a parameter's value")
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument(
            "--date", metavar="DATE", type=str, help="Override the event time"
        )
        subparser.add_argument(
            "parameter", metavar="PARAMETER", type=str, help="name of the parameter"
        ).completer = ParameterCompleter
        subparser.add_argument(
            "value", metavar="VALUE", type=str, help="value of the parameter"
        )
        subparser.set_defaults(func=self.set)

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

    def get(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)

        pval = processor.get_parameter_value(
            args.parameter, from_cache=not args.next, timeout=args.timeout
        )
        if pval and pval.eng_value is not None:
            val = pval.eng_value
            if isinstance(val, bool):
                print(str(val).lower())
            elif isinstance(val, (bytes, bytearray)):
                print(str(binascii.hexlify(val), "ascii"))
            else:
                print(val)

    def set(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)

        kwargs = {}
        if args.date:
            kwargs["generation_time"] = utils.parse_timestamp(args.date)

        processor.set_parameter_value(
            args.parameter,
            args.value,
            **kwargs,
        )
