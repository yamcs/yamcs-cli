from yamcs.client import YamcsClient

from yamcs.cli import utils
from yamcs.cli.completers import CommandCompleter, ProcessorCompleter


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
            "command", metavar="NAME", type=str, help="name of the command"
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
            "--processor", type=str, help="name of the processor", default="realtime"
        ).completer = ProcessorCompleter
        subparser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate the command, but do not queue it",
        )
        subparser.add_argument("-c", "--comment", help="attach a comment")

    def list_(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        mdb = client.get_mdb(opts.require_instance())

        rows = [["NAME", "DESCRIPTION", "ABSTRACT"]]
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
            with open(args.arg_file, "rb") as f:
                for arg in f.readlines():
                    arg = arg.strip()
                    if arg and not arg.startswith("#"):
                        self.add_argument(command_args, arg)

        for arg_arg in args.arg or []:
            for arg in arg_arg:
                self.add_argument(command_args, arg)

        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        instance = opts.require_instance()
        processor = client.get_processor(instance, args.processor)
        command = processor.issue_command(
            command=args.command,
            args=command_args,
            dry_run=args.dry_run,
            comment=args.comment,
        )
        print(command.id)
