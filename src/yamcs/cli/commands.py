from itertools import islice
from typing import Any, List

from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import CommandCompleter, ProcessorCompleter, StreamCompleter


class CommandsCommand(utils.Command):
    def __init__(self, parent):
        super(CommandsCommand, self).__init__(parent, "commands", "Manage commands")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List commands")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "describe", "Describe a command")
        subparser.add_argument(
            "command", metavar="NAME", type=str, help="name of the command"
        ).completer = CommandCompleter
        subparser.set_defaults(func=self.describe)

        subparser = self.create_subparser(subparsers, "run", "Run a command")
        subparser.set_defaults(func=self.run)
        subparser.add_argument(
            "command", metavar="NAME", type=str, help="Name of the command"
        ).completer = CommandCompleter
        subparser.add_argument("--arg-file", help="Read arguments from a file")
        subparser.add_argument(
            "--arg",
            metavar="ARG=VALUE",
            action="append",
            nargs="+",
            help="Set arguments",
        )
        subparser.add_argument(
            "--stream", type=str, help="Name of the stream"
        ).completer = StreamCompleter
        subparser.add_argument(
            "--processor", type=str, help="Name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument(
            "--sequence-number",
            metavar="SEQNO",
            type=int,
            help="Set a sequence number",
        )
        subparser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the command, but do not queue it",
        )
        subparser.add_argument("-c", "--comment", help="attach a comment")

        subparser = self.create_subparser(subparsers, "log", "Read command log")
        subparser.add_argument(
            "-n",
            "--lines",
            type=str,
            default=10,
            help="Number of commands to show",
        )
        subparser.add_argument(
            "-s",
            "--since",
            type=str,
            help="Include commands not older than the specified date",
        )
        subparser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Include commands not newer than the specified date",
        )
        subparser.set_defaults(func=self.log)

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())

        rows: List[List[Any]] = [["NAME", "DESCRIPTION", "ABSTRACT"]]
        for command in mdb.list_commands():
            rows.append(
                [
                    command.qualified_name,
                    command.description,
                    command.abstract,
                ]
            )
        utils.print_table(rows)

    def describe(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())
        command = mdb.get_command(args.command)
        print(command._proto)

    def add_argument(self, command_args, arg):
        if "=" not in arg:
            raise Exception(f"Invalid argument '{arg}'. Use format 'arg=value'")

        k, v = arg.split("=")
        command_args[k] = v

    def run(self, args):
        command_args = {}

        if args.arg_file:
            with open(args.arg_file, "rt") as f:
                for arg in f.readlines():
                    arg = arg.strip()
                    if arg and not arg.startswith("#"):
                        self.add_argument(command_args, arg)

        for arg_arg in args.arg or []:
            for arg in arg_arg:
                self.add_argument(command_args, arg)

        kwargs = {}
        if args.sequence_number is not None:
            kwargs["sequence_number"] = args.sequence_number

        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        command = processor.issue_command(
            command=args.command,
            args=command_args,
            dry_run=args.dry_run,
            comment=args.comment,
            stream=args.stream,
            **kwargs,
        )
        print(command.id)

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

        iterator = archive.list_command_history(
            descending=most_recent_only,
            start=start,
            stop=stop,
        )

        # Limit, unless explicit filters are set
        # We need to reverse it back to ascending in-memory.
        if most_recent_only:
            iterator = reversed(list(islice(iterator, 0, int(args.lines))))

        rows: List[List[Any]] = [["ID", "TIME", "COMMAND", "Q", "R", "S", "COMPLETION"]]
        for command in iterator:
            row = [command.id, command.generation_time, command.name]

            ack = command.acknowledgments.get("Acknowledge_Queued")
            row.append(ack.status if ack else "")

            ack = command.acknowledgments.get("Acknowledge_Released")
            row.append(ack.status if ack else "")

            ack = command.acknowledgments.get("Acknowledge_Sent")
            row.append(ack.status if ack else "")

            if command.is_success():
                row.append("SUCCESS")
            elif command.is_failure():
                row.append("FAILURE")
            else:
                row.append("")

            rows.append(row)
        utils.print_table(rows)
