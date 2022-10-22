from yamcs.cli import utils
from yamcs.cli.completers import ServiceCompleter
from yamcs.client import YamcsClient


class ServicesCommand(utils.Command):
    def __init__(self, parent):
        super(ServicesCommand, self).__init__(parent, "services", "Manage services")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List services")
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

        rows = [["NAME", "CLASS", "STATUS"]]
        for service in client.list_services(opts.require_instance()):
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
