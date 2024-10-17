import os
from itertools import islice
from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.utils import eprint


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

        subparser = self.create_subparser(subparsers, "log", "Read event log")
        subparser.add_argument(
            "-n",
            "--lines",
            type=str,
            default=10,
            help="Number of events to show",
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include events not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include events not newer than the specified date",
        )
        subparser.add_argument(
            "--filter",
            metavar="EXPRESSION",
            type=str,
            help="Apply a filter expression to each event",
        )
        subparser.set_defaults(func=self.log)

    def create(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)

        message = (args.message or "").strip()
        if not message:
            if "EDITOR" not in os.environ:
                eprint("*** $EDITOR not set")
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

    def log(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        archive = client.get_archive(opts.require_instance())

        start = None
        if args.since:
            start = utils.parse_timestamp(args.since)
        stop = None
        if args.until:
            stop = utils.parse_timestamp(args.until)

        most_recent_only = start is None and stop is None and args.lines != "all"

        iterator = archive.list_events(
            filter=args.filter,
            descending=most_recent_only,
            start=start,
            stop=stop,
        )

        # Limit, unless explicit filters are set
        # We need to reverse it back to ascending in-memory.
        if most_recent_only:
            iterator = reversed(list(islice(iterator, 0, int(args.lines))))

        rows: List[List[Any]] = [["SEVERITY", "TIME", "MESSAGE", "SOURCE", "TYPE"]]
        for event in iterator:
            row = [
                "-" if event.severity is None else event.severity,
                event.generation_time,
                "-" if event.message is None else event.message,
                "-" if event.source is None else event.source,
                "-" if event.event_type is None else event.event_type,
            ]
            rows.append(row)
        utils.print_table(rows)
