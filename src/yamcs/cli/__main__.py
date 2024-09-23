import argparse
import sys
import traceback

import argcomplete
import pkg_resources
from yamcs.client import Unauthorized

from yamcs.cli import utils
from yamcs.cli.alarms import AlarmsCommand
from yamcs.cli.algorithms import AlgorithmsCommand
from yamcs.cli.commands import CommandsCommand
from yamcs.cli.completers import InstanceCompleter
from yamcs.cli.config import ConfigCommand
from yamcs.cli.containers import ContainersCommand
from yamcs.cli.dbshell import DbShellCommand
from yamcs.cli.events import EventsCommand
from yamcs.cli.exceptions import NoInstanceError, NoServerError
from yamcs.cli.instances import InstancesCommand
from yamcs.cli.links import LinksCommand
from yamcs.cli.login import LoginCommand
from yamcs.cli.logout import LogoutCommand
from yamcs.cli.packets import PacketsCommand
from yamcs.cli.parameter_archive import ParameterArchiveCommand
from yamcs.cli.parameters import ParametersCommand
from yamcs.cli.processors import ProcessorsCommand
from yamcs.cli.rocksdb import RocksDBCommand
from yamcs.cli.services import ServicesCommand
from yamcs.cli.space_systems import SpaceSystemsCommand
from yamcs.cli.storage import StorageCommand
from yamcs.cli.streams import StreamsCommand
from yamcs.cli.tables import TablesCommand
from yamcs.cli.utils import eprint


def create_subparser(subparsers, command, help_):
    # Override the default help action so that it does not show up in
    # the usage string of every command
    subparser = subparsers.add_parser(command, help=help_, add_help=False)
    subparser.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS, help=argparse.SUPPRESS
    )
    return subparser


def main():
    parser = argparse.ArgumentParser(
        description=None,
        formatter_class=utils.SubCommandHelpFormatter,
        epilog="Run 'yamcs COMMAND --help' for more information on a command.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=utils.get_user_agent(),
        help="Print version information and quit",
    )
    parser.add_argument(
        "--instance",
        type=str,
        help="The Yamcs instance to use. Overrides the core/instance property",
    ).completer = InstanceCompleter
    parser.add_argument(
        "--debug",
        action="store_true",
        help=argparse.SUPPRESS,
    )

    # The width of this impacts the command width of the command column :-/
    metavar = "COMMAND"

    subparsers = parser.add_subparsers(title="Commands", metavar=metavar)
    subparsers.required = True

    AlarmsCommand(subparsers)
    AlgorithmsCommand(subparsers)
    CommandsCommand(subparsers)
    ConfigCommand(subparsers)
    ContainersCommand(subparsers)
    DbShellCommand(subparsers)
    EventsCommand(subparsers)
    InstancesCommand(subparsers)
    LinksCommand(subparsers)
    LoginCommand(subparsers)
    LogoutCommand(subparsers)
    PacketsCommand(subparsers)
    ParameterArchiveCommand(subparsers)
    ParametersCommand(subparsers)
    ProcessorsCommand(subparsers)
    RocksDBCommand(subparsers)
    ServicesCommand(subparsers)
    SpaceSystemsCommand(subparsers)
    StorageCommand(subparsers)
    StreamsCommand(subparsers)
    TablesCommand(subparsers)

    # Discover subcommand plugins
    for entry in pkg_resources.iter_entry_points(group="yamcs.cli.subcommands"):
        subcommand_cls = entry.load(subparsers)
        subcommand_cls(subparsers)

    # Provide bash autocompletion
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print()  # Clear prompt
    except NoServerError:
        eprint("No server. Run: 'yamcs login' to login to Yamcs")
        sys.exit(1)
    except NoInstanceError:
        eprint("No instance. Run: 'yamcs config set instance <instance>'")
        sys.exit(1)
    except Unauthorized:
        if args.debug:
            eprint(traceback.format_exc())
        eprint("Unauthorized. Run: 'yamcs login' to login to Yamcs")
        sys.exit(1)
    except Exception as e:
        if args.debug:
            eprint(traceback.format_exc())
        else:
            eprint(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
