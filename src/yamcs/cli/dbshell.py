import binascii
import cmd
import io
import json
import os
import readline
import sys
from collections import abc
from pydoc import pager
from typing import Any, List

from google.protobuf import json_format
from yamcs.client import YamcsClient, YamcsError
from yamcs.protobuf.events import events_pb2

from yamcs.cli import utils
from yamcs.cli.protobuf import (
    activities_pb2,
    cmdhistory_pb2,
    security_pb2,
    timeline_pb2,
)
from yamcs.cli.utils import eprint

SHOW_OPTIONS = ("databases", "engines", "streams", "tables", "stream")

PB_ACTIVITY_DEFINITION_TYPE = (
    "PROTOBUF(org.yamcs.activities.protobuf.ActivityDefinition)"
)
PB_ASSIGNMENT_TYPE = "PROTOBUF(org.yamcs.cmdhistory.protobuf.Cmdhistory$AssignmentInfo)"
PB_BANDFILTER_TYPE = "PROTOBUF(org.yamcs.timeline.protobuf.BandFilter)"
PB_EVENT_TYPE = "PROTOBUF(org.yamcs.yarch.protobuf.Db$Event)"
PB_USER_ACCOUNT_DETAIL_TYPE = (
    "PROTOBUF(org.yamcs.security.protobuf.UserAccountRecordDetail)"
)
PB_SERVICE_ACCOUNT_DETAIL_TYPE = (
    "PROTOBUF(org.yamcs.security.protobuf.ServiceAccountRecordDetail)"
)


class DbShellOptions:
    def __init__(self, args):
        self.interactive = not args.batch
        self.column_names = not args.skip_column_names
        self.binary_as_hex = not args.batch or args.binary_as_hex
        self.histfile = os.path.join(utils.CONFIG_DIR, "history")

        if args.batch or args.command:
            self.histfile = None


class DbShellCommand(utils.Command):
    def __init__(self, parent):
        super(DbShellCommand, self).__init__(
            parent, "dbshell", "Launch Yamcs DB Shell", add_epilog=False
        )

        self.parser.set_defaults(func=self.launch)
        self.parser.add_argument(
            "-c", "--command", metavar="COMMAND", type=str, help="SQL command string"
        )
        self.parser.add_argument(
            "-N",
            "--skip-column-names",
            action="store_true",
            help="Don't print column names",
        )
        self.parser.add_argument(
            "-B",
            "--batch",
            action="store_true",
            help="Don't use history file. Disable interactive behavior",
        )
        self.parser.add_argument(
            "--binary-as-hex", action="store_true", help="Display binary values as hex"
        )

    def launch(self, args):
        opts = utils.CommandOptions(args)
        client = YamcsClient(**opts.client_kwargs)
        shell_opts = DbShellOptions(args)

        shell = DbShell(client, opts=shell_opts)
        shell.do_use(opts.require_instance())
        if args.command:
            shell.onecmd(args.command)
        else:
            if shell_opts.interactive:
                server_info = client.get_server_info()
                intro = (
                    "Yamcs DB Shell\n"
                    "Server version: {} - ID: {}\n\n"
                    "Type help or ? for help.\n"
                ).format(server_info.version, server_info.id)
                shell.cmdloop(intro)
            else:
                shell.cmdloop()


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

    def __init__(self, columns, column_types, output, opts):
        self.columns = columns
        self.column_types = column_types
        self.opts = opts
        if opts.column_names:
            self.widths = [len(name) for name in columns]
        else:
            self.widths = [0 for _ in columns]
        self.separator = ""
        self.pending_rows: List[List[Any]] = []
        self.output = output
        self.printed_row_count = 0
        self.delimiter = ";"

    def add(self, row):
        print_row: List[Any] = []
        for i, value in enumerate(row):
            if value is None:
                string_value = "NULL"
            elif self.column_types[i] == PB_ACTIVITY_DEFINITION_TYPE:
                pb = activities_pb2.ActivityDefinition()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif self.column_types[i] == PB_ASSIGNMENT_TYPE:
                pb = cmdhistory_pb2.AssignmentInfo()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif self.column_types[i] == PB_BANDFILTER_TYPE:
                pb = timeline_pb2.BandFilter()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif self.column_types[i] == PB_EVENT_TYPE:
                pb = events_pb2.Event()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif self.column_types[i] == PB_SERVICE_ACCOUNT_DETAIL_TYPE:
                pb = security_pb2.ServiceAccountRecordDetail()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif self.column_types[i] == PB_USER_ACCOUNT_DETAIL_TYPE:
                pb = security_pb2.UserAccountRecordDetail()
                pb.ParseFromString(value)
                dict_value = json_format.MessageToDict(pb)  # type: ignore
                string_value = json.dumps(dict_value)
            elif isinstance(value, (bytes, bytearray)):
                if self.opts.binary_as_hex:
                    string_value = "0x" + str(binascii.hexlify(value), "ascii")
                else:
                    string_value = value  # Raw bytes
            elif isinstance(value, abc.Mapping):
                string_value = json.dumps(value)
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
            if self.opts.column_names:
                if self.opts.interactive:
                    print(separator, file=self.output)
                    print(fm.format(*self.columns), file=self.output)
                else:
                    print("\t".join(self.columns), file=self.output)
            if self.opts.interactive:
                print(separator, file=self.output)

        for row in self.pending_rows:
            if self.opts.interactive:
                print(fm.format(*row), file=self.output)
            else:
                if self.opts.binary_as_hex:
                    print("\t".join(row), file=self.output)
                else:
                    for idx, el in enumerate(row):
                        if idx != 0:
                            self.output.write("\t")
                        if isinstance(el, (bytes, bytearray)):
                            self.output.buffer.write(el)
                        else:
                            self.output.write(el)
                    self.output.write("\n")
            self.printed_row_count += 1
        self.pending_rows = []

    def print_summary(self):
        if self.opts.interactive:
            print(self.generate_separator(), file=self.output)
            if self.printed_row_count == 1:
                print("1 row in set\n", file=self.output)
            else:
                print(
                    "{} rows in set\n".format(self.printed_row_count), file=self.output
                )

    def generate_separator(self):
        separator = ""
        for width in self.widths:
            separator += "+-" + (width * "-") + "-"
        separator += "+"
        return separator


class DbShell(cmd.Cmd):
    def __init__(self, client, opts):
        cmd.Cmd.__init__(self)
        self._client = client
        self.opts = opts
        self.pager = False
        self.instance = None
        self.prompt = "> " if opts.interactive else ""
        self.delimiter = ";"
        self.tables = []
        self.streams = []

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            print("List of dbshell commands:")
            rows: List[List[Any]] = [["?", "(\\?) Show help."]]
            for command in cmds:
                if command == "EOF":  # Don't document EOF
                    continue
                doc = getattr(self, "do_" + command).__doc__
                if doc:
                    rows.append([command, doc])
            utils.print_table(rows)
            print()

    def emptyline(self):
        pass  # Override default behaviour of repeating the last command

    def do_delimiter(self, args):
        """(\\d) Set statement delimiter."""
        if not args:
            eprint("*** Delimiter not set")
        else:
            self.delimiter = args

    def do_status(self, args):
        """(\\s) Print status information."""
        rows: List[List[Any]] = []
        rows.append(["Current instance:", self.instance])
        rows.append(["Pager:", "yes" if self.pager else "no"])
        rows.append(["Using delimiter:", self.delimiter])
        utils.print_table(rows, header=False)

    def do_use(self, args):
        """(\\u) Use another instance, provided as argument."""
        self.instance = args
        self.prompt = self.instance + "> " if self.opts.interactive else ""
        self.do_rehash(None)

    def do_pager(self, args):
        """(\\P) Print results to a pager."""
        self.pager = True

    def do_nopager(self, args):
        """(\\n) Disable pager. Results are printed to stdout."""
        self.pager = False

    def complete_show(self, text, line, begidx, endidx):
        return [o for o in SHOW_OPTIONS if o.startswith(text)]

    def complete_describe(self, text, line, begidx, endidx):
        return [o for o in (self.streams + self.tables) if o.startswith(text)]

    def default(self, line):
        try:
            if line.startswith("\\"):
                if self.run_command(line):
                    return True
            else:
                for statement in line.split(self.delimiter):
                    if not statement:
                        continue

                    archive = self._client.get_archive(self.instance)
                    results = archive.execute_sql(statement)
                    self.paginate(results)
        except YamcsError as e:
            eprint(e)
            sys.exit(1)

    def run_command(self, command):
        if command == "\\":
            pass
        else:
            parts = command.split(None, 1)
            command = parts[0][:2]
            args = parts[1] if len(parts) == 2 else None

            if command == "\\?":
                self.do_help(args)
            elif command == "\\!":
                self.do_system(args)
            elif command == "\\#":
                self.do_rehash(args)
            elif command == "\\.":
                self.do_source(args)
            elif command == "\\d":
                self.do_delimiter(args)
            elif command == "\\e":
                self.do_edit(args)
            elif command == "\\h":
                self.do_help(args)
            elif command == "\\n":
                self.do_nopager(args)
            elif command == "\\q":
                return self.do_quit(args)
            elif command == "\\s":
                self.do_status(args)
            elif command == "\\u":
                self.do_use(args)
            elif command == "\\P":
                self.do_pager(args)
            else:
                eprint(f"*** Unknown command '{command}'")

    def do_edit(self, args):
        """(\\e) Edit a command with $EDITOR."""
        if "EDITOR" not in os.environ:
            eprint("*** $EDITOR not set")
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

    def do_source(self, args):
        """(\\.) Execute an SQL script file, provided as argument."""
        if not args:
            eprint("*** Usage: \\. <filename> | source <filename>")
        else:
            try:
                with open(args, "rt") as f:
                    for sql in f.readlines():
                        self.default(sql)
            except OSError as e:
                eprint("***", e)

    def do_rehash(self, args):
        """(\\#) Rebuild completion hash."""
        archive = self._client.get_archive(self.instance)
        self.streams = [s.name for s in archive.list_streams()]
        self.tables = [t.name for t in archive.list_tables()]

    def do_exit(self, args):
        """(\\q) Synonym for quit."""
        return self.do_quit(args)

    def do_quit(self, args):
        """(\\q) Quits the DB Shell."""
        return True

    def do_EOF(self, line):  # Handles CTRL-D
        """Quits the DB Shell."""
        print()  # Newline to remove prompt
        return True

    def do_help(self, args):
        """(\\h) Display this help."""
        return super(DbShell, self).do_help(args)

    def do_system(self, args):
        """(\\!) Execute a system command."""
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
                    results.columns,
                    results.column_types,
                    output,
                    opts=self.opts,
                )
            assert printer
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
        elif self.opts.interactive:
            print("Empty set\n", file=output)

    def preloop(self):
        if self.opts.histfile and os.path.exists(self.opts.histfile):
            readline.read_history_file(self.opts.histfile)

    def postloop(self):
        if self.opts.histfile:
            readline.set_history_length(200)
            readline.write_history_file(self.opts.histfile)

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
