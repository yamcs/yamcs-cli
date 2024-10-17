import argparse
import json
import os
import sys
from configparser import ConfigParser
from datetime import datetime, timedelta, timezone
from typing import Any, List

import pkg_resources
from dateutil import parser
from yamcs.client import Credentials, parse_server_timestring, to_isostring

from yamcs.cli.exceptions import NoInstanceError, NoServerError

HOME = os.path.expanduser("~")
CONFIG_DIR = os.path.join(os.path.join(HOME, ".config"), "yamcs-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials")


def get_user_agent():
    dist = pkg_resources.get_distribution("yamcs-cli")
    return "Yamcs CLI v" + dist.version


def read_config():
    config = ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    return config


def save_config(config):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_FILE, "wt") as f:
        config.write(f)


def save_credentials(credentials: Credentials):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(CREDENTIALS_FILE, "wt") as f:
        obj = {
            "access_token": credentials.access_token,
            "refresh_token": credentials.refresh_token,
        }
        if credentials.expiry:
            obj["expiry"] = to_isostring(credentials.expiry)
        json.dump(obj, f, indent=2)


def read_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rt") as f:
            try:
                d = json.load(f)
            except json.JSONDecodeError:
                return None
            access_token = d["access_token"]
            refresh_token = d["refresh_token"]
            expiry = parse_server_timestring(d["expiry"]) if "expiry" in d else None
            return Credentials(
                access_token=access_token,
                refresh_token=refresh_token,
                expiry=expiry,
            )
    return None


def clear_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)
        return True
    return False


def print_table(rows: List[List[Any]], decorate=False, header=False):
    if not rows:
        return

    widths = list(map(len, rows[0]))
    for row in rows:
        for idx, col in enumerate(row):
            widths[idx] = max(len(str(col)), widths[idx])

    separator = "  "
    prefix = "| " if decorate else ""
    suffix = " |" if decorate else ""

    total_width = len(prefix) + len(suffix)
    for width in widths:
        total_width += width
    total_width += len(separator) * (len(widths) - 1)

    data = rows[1:] if header else rows
    if header and data:
        if decorate:
            print("+{}+".format("-" * (total_width - 2)))
        cols = separator.join(
            [str.ljust(str(col), width) for col, width in zip(rows[0], widths)]
        )
        print(prefix + cols + suffix)
    if data:
        if decorate:
            print("+{}+".format("-" * (total_width - 2)))
        for row in data:
            cols = separator.join(
                [str.ljust(str(col), width) for col, width in zip(row, widths)]
            )
            print(prefix + cols + suffix)
        if decorate:
            print("+{}+".format("-" * (total_width - 2)))


def parse_timestamp(timestamp):
    utc = False
    if timestamp.lower().endswith(" utc"):
        utc = True
        timestamp = timestamp[:-4]

    tz = timezone.utc if utc else None
    now = datetime.now().astimezone(tz=tz)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if timestamp == "now":
        return now
    elif timestamp == "today":
        return today
    elif timestamp == "yesterday":
        return today - timedelta(days=1)
    elif timestamp == "tomorrow":
        return today + timedelta(days=1)

    # Switch to datetime.fromisoformat when dropping Python 3.6
    parsed = parser.isoparse(timestamp)
    return parsed if parsed.tzinfo else parsed.astimezone(tz=tz)


def eprint(*args, **kwargs):
    """Print to stderr instead of stdout."""
    print(*args, file=sys.stderr, **kwargs)


def parse_ys_url(url: str):
    parts = url[5:].split("/", 1)
    if len(parts) == 2 and parts[1]:
        if parts[1] == "/":
            return parts[0], None
        else:
            return parts[0], parts[1]
    else:
        return parts[0], None


class Command:
    config_options = ["core.url", "core.instance", "core.enable_utc"]

    def __init__(self, subparsers, command, help_, add_epilog=True):
        self.parser = self.create_subparser(
            subparsers, command, help_, add_epilog=add_epilog
        )

    def create_subparser(self, subparsers, command, help_, add_epilog=True):
        epilog = None
        if add_epilog:
            epilog = (
                "Run 'yamcs {} COMMAND --help' "
                "for more information on a command.".format(command)
            )

        # Override the default help action so that it does not show up in
        subparser = subparsers.add_parser(
            command,
            help=help_,
            add_help=False,
            formatter_class=SubCommandHelpFormatter,
            epilog=epilog,
        )
        # the usage string of every command
        subparser.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help=argparse.SUPPRESS,
        )
        return subparser

    def register_config_option(self, option):
        """
        Add to the list of known config settings
        """
        if not option:
            raise ValueError("Empty option")
        if "." not in option:
            raise ValueError("Missing section")
        if option.startswith("core."):
            raise ValueError("Extensions cannot add core options")
        if option not in Command.config_options:
            Command.config_options.append(option)


class CommandOptions:
    def __init__(self, args):
        self.config = read_config()
        self._credentials = read_credentials()
        self._args = args

        if self.enable_utc:
            os.environ["PYTHON_YAMCS_CLIENT_UTC"] = "1"

    @property
    def instance(self):
        return self._args.instance or (
            self.config.has_section("core")
            and self.config.get("core", "instance", fallback=None)
        )

    @property
    def url(self):
        if self.config.has_section("core"):
            return self.config.get("core", "url", fallback=None)
        return None

    @property
    def enable_utc(self):
        if self.config.has_section("core"):
            return self.config.getboolean("core", "enable_utc", fallback=False)
        return False

    @property
    def user_agent(self):
        return get_user_agent()

    def require_instance(self):
        if not self.instance:
            raise NoInstanceError()
        return self.instance

    def _on_token_update(self, credentials):
        save_credentials(credentials)

    @property
    def client_kwargs(self):
        if not self.url:
            raise NoServerError
        return {
            "address": self.url,
            "tls_verify": False,
            "user_agent": self.user_agent,
            "credentials": self._credentials,
            "on_token_update": self._on_token_update,
        }


class SubCommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        # Removes the subparsers metavar from the help output
        parts = super(SubCommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts
