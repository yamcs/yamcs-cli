from yamcs.cli import utils
from yamcs.cli.completers import LinkCompleter
from yamcs.client import YamcsClient


class LinksCommand(utils.Command):
    def __init__(self, parent):
        super(LinksCommand, self).__init__(parent, "links", "Manage data links")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List data links")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "describe", "Describe a link")
        subparser.add_argument(
            "link", metavar="LINK", type=str, help="name of the link"
        ).completer = LinkCompleter
        subparser.set_defaults(func=self.describe)

        subparser = self.create_subparser(subparsers, "enable", "Enable a link")
        subparser.add_argument(
            "links", metavar="LINK", type=str, nargs="+", help="name of the link"
        ).completer = LinkCompleter
        subparser.set_defaults(func=self.enable)

        subparser = self.create_subparser(subparsers, "disable", "Disable a link")
        subparser.add_argument(
            "links", metavar="LINK", type=str, nargs="+", help="name of the link"
        ).completer = LinkCompleter
        subparser.set_defaults(func=self.disable)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        rows = [["NAME", "CLASS", "STATUS", "IN", "OUT"]]
        for link in client.list_links(opts.require_instance()):
            rows.append(
                [
                    link.name,
                    link.class_name,
                    link.status,
                    link.in_count,
                    link.out_count,
                ]
            )
        utils.print_table(rows)

    def enable(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for link_name in args.links:
            link = client.get_link(opts.require_instance(), link_name)
            link.enable_link()

    def disable(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        for link_name in args.links:
            link = client.get_link(opts.require_instance(), link_name)
            link.disable_link()

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        link = client.get_link(opts.require_instance(), args.link)
        print(link.get_info())
