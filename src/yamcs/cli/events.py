import os

from yamcs.cli import utils
from yamcs.client import YamcsClient


class EventsCommand(utils.Command):
    def __init__(self, parent):
        super(EventsCommand, self).__init__(parent, "events", "Create events")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "create", "Create an event")
        subparser.add_argument(
            "-m", "--message", metavar="MESSAGE", type=str, help="event message"
        )
        subparser.add_argument(
            "--date", metavar="DATE", type=str, help="Override the event time"
        )
        subparser.add_argument(
            "--sequence-number",
            metavar="SEQNO",
            type=int,
            help="Set a sequence number",
        )
        subparser.add_argument(
            "--severity",
            metavar="LEVEL",
            type=str,
            help="Set severity",
            choices=["info", "watch", "warning", "distress", "critical", "severe"],
            default="info",
        )
        subparser.add_argument(
            "--source", metavar="SOURCE", type=str, help="event source"
        )
        subparser.add_argument("--type", metavar="TYPE", type=str, help="event type")
        subparser.add_argument(
            "--extra",
            metavar="KEY=VALUE",
            action="append",
            nargs="+",
            help="Set additional event properties",
        )

        subparser.set_defaults(func=self.create)

    def create(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        message = (args.message or "").strip()
        if not message:
            if "EDITOR" not in os.environ:
                print("*** $EDITOR not set")
                return False
            path = os.path.join(utils.CONFIG_DIR, "event")
            cmd = os.environ["EDITOR"]
            try:
                os.system(cmd + " " + path)
                if os.path.exists(path):
                    with open(path, "r") as f:
                        message = f.read().strip()
            finally:
                if os.path.exists(path):
                    os.remove(path)

        if message:
            kwargs = {}
            if args.source:
                kwargs["source"] = args.source
            if args.type:
                kwargs["event_type"] = args.type
            if args.date:
                kwargs["time"] = utils.parse_timestamp(args.date)
            if args.sequence_number is not None:
                kwargs["sequence_number"] = args.sequence_number

            if args.extra:
                kwargs["extra"] = {}
                for extra_arg in args.extra:
                    for extra in extra_arg:
                        if "=" not in extra:
                            raise ValueError(
                                f"Invalid parameter '{extra}'. Use format 'key=value'"
                            )
                        key, value = extra.split("=")
                        kwargs["extra"][key] = value

            client.send_event(
                instance=opts.require_instance(),
                message=message,
                severity=args.severity,
                **kwargs,
            )
