import binascii
import cmd
import io
import os
import sys
from pydoc import pager

from yamcs.cli import utils
from yamcs.client import YamcsClient
from yamcs.core.exceptions import YamcsError

SHOW_OPTIONS = ("databases", "engines", "streams", "tables", "stream")


class DbShellCommand(utils.Command):
    def __init__(self, parent):
        super(DbShellCommand, self).__init__(
            parent, "dbshell", "Launch Yamcs DB Shell", add_epilog=False
        )

        self.parser.set_defaults(func=self.launch)
        self.parser.add_argument(
            "-c", "--command", metavar="COMMAND", type=str, help="SQL command string"
        )

    def launch(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        shell = DbShell(client)
        shell.do_use(opts.instance)
        if args.command:
            shell.onecmd(args.command)
        else:
            server_info = client.get_server_info()
            intro = (
                "Yamcs DB Shell\n"
                "Server version: {} - ID: {}\n\n"
                "Type "
                "help"
                " or "
                "?"
                " for help.\n"
            ).format(server_info.version, server_info.id)
            shell.cmdloop(intro)


class ResultSetPrinter:
    """
    Capable of printing tabulated records. Print operations
    must be manually triggered by the using code. Each print
    may lead to an enlargement of the column widths from the
    previous print operation.

    Note that this was written such that it could be reused
    for following a StreamSQL stream too when that actually
    has server-side SQL support.
    """

    def __init__(self, columns, column_types, output):
        self.columns = columns
        self.column_types = column_types
        self.widths = [len(name) for name in columns]
        self.separator = ""
        self.pending_rows = []
        self.output = output
        self.printed_row_count = 0

    def add(self, row):
        print_row = []
        for i, value in enumerate(row):
            if isinstance(value, (bytes, bytearray)):
                string_value = "0x" + str(binascii.hexlify(value), "ascii")
            else:
                string_value = str(value)
            print_row.append(string_value)
            self.widths[i] = max(len(string_value), self.widths[i])
        self.pending_rows.append(print_row)

    def print_pending(self):
        fm = ""
        for i, width in enumerate(self.widths):
            fm += "| {" + str(i) + ":" + str(width) + "} "
        fm += "|"

        if self.printed_row_count == 0:
            separator = self.generate_separator()
            print(separator, file=self.output)
            print(fm.format(*self.columns), file=self.output)
            print(separator, file=self.output)

        for row in self.pending_rows:
            print(fm.format(*row), file=self.output)
            self.printed_row_count += 1
        self.pending_rows = []

    def print_summary(self):
        print(self.generate_separator(), file=self.output)
        if self.printed_row_count == 1:
            print("1 row in set\n", file=self.output)
        else:
            print("{} rows in set\n".format(self.printed_row_count), file=self.output)

    def generate_separator(self):
        separator = ""
        for width in self.widths:
            separator += "+-" + (width * "-") + "-"
        separator += "+"
        return separator


class DbShell(cmd.Cmd):

    pager = False
    prompt = "> "
    instance = None

    tables = []
    streams = []

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self._client = client

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            print("List of dbshell commands:")
            rows = [["?", "Show help."]]
            for command in cmds:
                doc = getattr(self, "do_" + command).__doc__
                if doc:
                    rows.append([command, doc])
            utils.print_table(rows)
            print()

    def emptyline(self):
        pass  # Override default behaviour of repeating the last command

    def do_use(self, args):
        """Use another instance, provided as argument."""
        self.instance = args
        self.prompt = self.instance + "> "

        archive = self._client.get_archive(self.instance)
        self.streams = [s.name for s in archive.list_streams()]
        self.tables = [t.name for t in archive.list_tables()]

    def do_pager(self, args):
        """Print results to a pager."""
        self.pager = True

    def do_nopager(self, args):
        """Disable pager. Results are printed to stdout."""
        self.pager = False

    def complete_show(self, text, line, begidx, endidx):
        return [o for o in SHOW_OPTIONS if o.startswith(text)]

    def complete_describe(self, text, line, begidx, endidx):
        return [o for o in (self.streams + self.tables) if o.startswith(text)]

    def default(self, line):
        try:
            for statement in line.split(";"):
                if not statement:
                    continue

                archive = self._client.get_archive(self.instance)
                results = archive.execute_sql(statement)
                self.paginate(results)
        except YamcsError as e:
            print(e)

    def do_edit(self, args):
        """Edit a command with $EDITOR."""
        if "EDITOR" not in os.environ:
            print("*** $EDITOR not set")
        else:
            path = os.path.join(utils.CONFIG_DIR, "sql")
            cmd = os.environ["EDITOR"]
            try:
                os.system(cmd + " " + path)
                if os.path.exists(path):
                    with open(path, "r") as f:
                        sql = f.read()
                        if sql:
                            self.default(sql)
            finally:
                if os.path.exists(path):
                    os.remove(path)

    def do_exit(self, args):
        """Synonym for quit."""
        return self.do_quit(args)

    def do_quit(self, args):
        """Quits the DB Shell."""
        return True

    def do_EOF(self, line):  # Handles CTRL-D
        """Quits the DB Shell."""
        print()  # Newline to remove prompt
        return True

    def do_system(self, args):
        """Execute a system command."""
        os.system(args)

    def paginate(self, results):
        if self.pager:
            # TODO this will blow up with large result sets.
            # But it's best fixed server-side where we should
            # implement resume tokens on result sets, and fetch
            # them one by one, rather than pushing the entire
            # data set.
            output = io.StringIO()
        else:
            output = sys.stdout

        self.print_results(results, output)

        if self.pager:
            output.seek(0)
            pager(output.read())

    def print_results(self, results, output):
        """
        Prints a result set for a static tuple source.
        This will not give good behaviour for a results that come
        in live from a StreamSQL stream, because it buffers.
        """
        printer = None
        for i, row in enumerate(results):
            if i == 0:
                printer = ResultSetPrinter(
                    results.columns, results.column_types, output
                )
            printer.add(row)

            # When we have a decent amount, print the results.
            # The actual value is not so important. The higher the
            # less column widths will shift, but it will also use
            # a bit more memory.
            if len(printer.pending_rows) > 100:
                printer.print_pending()

        if printer:
            printer.print_pending()
            printer.print_summary()
        else:
            print("Empty set\n", file=output)

    def cmdloop(self, *args, **kwargs):
        # Monkey-patch so that ctrl-c on cmd.Cmd does not quit
        # the dbshell, but just cancels the current input
        def interruptable_input(_input):
            def _interruptable_input(*args):
                try:
                    return _input(*args)
                except KeyboardInterrupt:
                    print()
                    return "\n"

            return _interruptable_input

        input_fn = cmd.__builtins__["input"]
        cmd.__builtins__["input"] = interruptable_input(input_fn)
        super().cmdloop(*args, **kwargs)
