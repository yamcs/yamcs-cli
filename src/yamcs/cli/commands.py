from yamcs.cli import utils
from yamcs.cli.completers import CommandCompleter
from yamcs.client import YamcsClient


class CommandsCommand(utils.Command):
    def __init__(self, parent):
        super(CommandsCommand, self).__init__(parent, "commands", "Read commands")

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List commands")
        subparser.set_defaults(func=self.list_)

        subparser = self.create_subparser(subparsers, "describe", "Describe a command")
        subparser.add_argument(
            "command", metavar="NAME", type=str, help="name of the command"
        ).completer = CommandCompleter
        subparser.set_defaults(func=self.describe)

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
