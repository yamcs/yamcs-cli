from itertools import islice
from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import ProcessorCompleter


class AlarmsCommand(utils.Command):
    def __init__(self, parent):
        super(AlarmsCommand, self).__init__(parent, "alarms", "Manage alarms")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        # list
        subparser = self.create_subparser(subparsers, "list", "Show active alarms")
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.set_defaults(func=self.list_)

        # acknowledge
        subparser = self.create_subparser(
            subparsers, "acknowledge", "Acknowledge an alarm"
        )
        subparser.add_argument(
            "alarm", metavar="ALARM", type=str, help="name of the alarm"
        )
        subparser.add_argument(
            "seqno", metavar="SEQNO", type=int, help="alarm sequence number"
        )
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument("-c", "--comment", type=str, help="attach a comment")
        subparser.set_defaults(func=self.acknowledge)

        # shelve
        subparser = self.create_subparser(subparsers, "shelve", "Shelve an alarm")
        subparser.add_argument(
            "alarm", metavar="ALARM", type=str, help="name of the alarm"
        )
        subparser.add_argument(
            "seqno", metavar="SEQNO", type=int, help="alarm sequence number"
        )
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument("-c", "--comment", type=str, help="attach a comment")
        subparser.set_defaults(func=self.shelve)

        # unshelve
        subparser = self.create_subparser(subparsers, "unshelve", "Unshelve an alarm")
        subparser.add_argument(
            "alarm", metavar="ALARM", type=str, help="name of the alarm"
        )
        subparser.add_argument(
            "seqno", metavar="SEQNO", type=int, help="alarm sequence number"
        )
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument("-c", "--comment", type=str, help="attach a comment")
        subparser.set_defaults(func=self.unshelve)

        # clear
        subparser = self.create_subparser(subparsers, "clear", "Clear an alarm")
        subparser.add_argument(
            "alarm", metavar="ALARM", type=str, help="name of the alarm"
        )
        subparser.add_argument(
            "seqno", metavar="SEQNO", type=int, help="alarm sequence number"
        )
        subparser.add_argument(
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument("-c", "--comment", type=str, help="attach a comment")
        subparser.set_defaults(func=self.clear)

        # log
        subparser = self.create_subparser(subparsers, "log", "Read alarm log")
        subparser.add_argument(
            "-a",
            "--alarm",
            type=str,
            help="Filter by alarm name",
        )
        subparser.add_argument(
            "-n",
            "--lines",
            type=str,
            default=10,
            help="Number of alarms to show",
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include alarms not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include alarms not newer than the specified date",
        )
        subparser.set_defaults(func=self.log)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)

        rows: List[List[Any]] = [["TIME", "NAME", "SEQNO", "SEVERITY"]]
        for alarm in processor.list_alarms():
            row = [
                alarm.trigger_time,
                alarm.name,
                alarm.sequence_number,
                alarm.severity,
            ]
            rows.append(row)
        utils.print_table(rows)

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

        iterator = archive.list_alarms(
            name=args.alarm,
            descending=most_recent_only,
            start=start,
            stop=stop,
        )

        # Limit, unless explicit filters are set
        # We need to reverse it back to ascending in-memory.
        if most_recent_only:
            iterator = reversed(list(islice(iterator, 0, int(args.lines))))

        rows: List[List[Any]] = [["TIME", "NAME", "SEQNO", "SEVERITY"]]
        for alarm in iterator:
            row = [
                alarm.trigger_time,
                alarm.name,
                alarm.sequence_number,
                alarm.severity,
            ]
            rows.append(row)
        utils.print_table(rows)

    def acknowledge(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        processor.acknowledge_alarm(args.alarm, args.seqno, comment=args.comment)

    def shelve(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        processor.shelve_alarm(args.alarm, args.seqno, comment=args.comment)

    def unshelve(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        processor.unshelve_alarm(args.alarm, args.seqno, comment=args.comment)

    def clear(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        processor.clear_alarm(args.alarm, args.seqno, comment=args.comment)
