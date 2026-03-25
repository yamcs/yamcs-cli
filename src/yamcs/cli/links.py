import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Link, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import LinkCompleter


class LinksCommand(utils.Command):
    def __init__(self, parent):
        super(LinksCommand, self).__init__(parent, "links", "Manage data links")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List data links")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
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

        subparser = self.create_subparser(
            subparsers, "run-action", "Run a custom link action"
        )
        subparser.add_argument(
            "link", metavar="LINK", type=str, help="name of the link"
        ).completer = LinkCompleter
        subparser.add_argument(
            "action", metavar="ACTION", type=str, help="name of the action"
        )
        subparser.set_defaults(func=self.run_action)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        iterator = client.list_links(opts.require_instance())
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Link]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Link]):
        rows: List[List[Any]] = [["NAME", "CLASS", "STATUS", "IN", "OUT"]]
        for link in iterator:
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

    def run_action(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        link = client.get_link(opts.require_instance(), args.link)
        link.run_action(args.action)
