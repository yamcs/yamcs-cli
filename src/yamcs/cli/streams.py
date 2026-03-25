import json
from typing import Any, Iterable, List

from google.protobuf.json_format import MessageToJson
from yamcs.client import Stream, YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import StreamCompleter


class StreamsCommand(utils.Command):
    def __init__(self, parent):
        super(StreamsCommand, self).__init__(parent, "streams", "Read streams")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List streams")
        subparser.add_argument(
            "--format",
            dest="format",
            type=str,
            help="Format for printing",
            choices=["table", "json"],
            default="table",
        )
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "describe", "Describe a stream")
        subparser.add_argument(
            "stream", metavar="STREAM", type=str, help="name of the stream"
        ).completer = StreamCompleter
        subparser.set_defaults(func=self.describe)

        subparser = self.create_subparser(
            subparsers, "subscribe", "Subscribe to a stream"
        )
        subparser.add_argument(
            "stream", metavar="STREAM", type=str, help="name of the stream"
        ).completer = StreamCompleter
        # subparser.add_argument(
        #    "--limit",
        #    type=int,
        #    help="Maximum number of updates. Default is unlimited."
        # )
        subparser.set_defaults(func=self.subscribe)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())
        iterator = archive.list_streams()
        if args.format == "json":
            self.list_json(iterator)
        else:
            self.list_table(iterator)

    def list_json(self, iterator: Iterable[Stream]):
        msg_array = [MessageToJson(x._proto, indent=2) for x in iterator]
        json_array = json.loads("[" + ",".join(msg_array) + "]")
        print(json.dumps(json_array, indent=2))

    def list_table(self, iterator: Iterable[Stream]):
        rows: List[List[Any]] = [["NAME"]]
        for stream in iterator:
            rows.append([stream.name])
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())
        stream = archive.get_stream(args.stream)
        print(stream._proto)

    def subscribe(self, args):
        def on_data(stream_data):
            print(stream_data._proto)

        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())
        try:
            subscription = archive.create_stream_subscription(
                args.stream, on_data=on_data
            )
            subscription.result()
        except KeyboardInterrupt:
            pass
