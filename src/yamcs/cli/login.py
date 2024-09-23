import os
from getpass import getpass
from typing import Optional

from yamcs.client import Credentials, YamcsClient

from yamcs.cli import utils
from yamcs.cli.utils import eprint


class LoginCommand(utils.Command):
    def __init__(self, parent):
        super(LoginCommand, self).__init__(parent, "login", "Login to a Yamcs server")

        self.parser.set_defaults(func=self.do_login)
        self.parser.add_argument(
            "url",
            metavar="URL",
            nargs="?",
            type=str,
            help="server URL (example: http://localhost:8090)",
        )
        self.parser.add_argument(
            "--kerberos",
            action="store_true",
            help="Authenticate using Kerberos negotiation",
        )
        self.parser.add_argument(
            "-u",
            "--username",
            help="Username",
        )
        self.parser.add_argument(
            "--instance",
            dest="preferred_instance",
            help="Selected instance",
        )

    def do_login(self, args):
        opts = utils.CommandOptions(args)

        url = args.url or self.read_url(opts)

        client_kwargs = {
            "address": url,
            "tls_verify": False,
        }

        # First a simple client without any auth (some paths are unprotected)
        client = YamcsClient(**client_kwargs)

        if args.kerberos:
            try:
                from yamcs.kerberos import KerberosCredentials  # type: ignore
            except ImportError:
                eprint(
                    "*** Missing Kerberos support. This is included in "
                    "the optional package: yamcs-client-kerberos"
                )
                return False

            credentials = KerberosCredentials()
            client = YamcsClient(credentials=credentials, **client_kwargs)
            eprint("Login succeeded")
        elif args.username:
            credentials = self.read_credentials(username=args.username)
            if credentials:
                client = YamcsClient(credentials=credentials, **client_kwargs)
                eprint("Login succeeded")
            else:
                return
        elif client.get_auth_info().require_authentication:
            credentials = self.read_credentials()
            if credentials:
                client = YamcsClient(credentials=credentials, **client_kwargs)
                eprint("Login succeeded")
            else:
                return
        else:
            user_info = client.get_user_info()
            eprint(
                "Anonymous login succeeded (username: {})".format(user_info.username)
            )

        # Allow to influence the instance selection.
        #
        # Either from the top-level "instance" argument, or (more importantly)
        # from the option on this subcommand.
        #
        # If nothing is specified, a somewhat random instance is selected
        # (the first in the list).
        preferred_instance = args.preferred_instance or args.instance

        self.save_client_config(client, opts.config, preferred_instance)

    def read_url(self, opts):
        default_url = opts.url or "http://localhost:8090"
        return input("URL [{}]: ".format(default_url)) or default_url

    def read_credentials(self, username=None):
        if username is None:
            username = input("Username: ")
        if not username:
            eprint("*** Username may not be empty")
            return False

        password = os.environ.get("YAMCS_CLI_PASSWORD")
        if password is None:
            password = getpass("Password: ")
        if not password:
            eprint("*** Password may not be empty")
            return False

        return Credentials(username=username, password=password)

    def save_client_config(
        self,
        client: YamcsClient,
        config,
        preferred_instance: Optional[str],
    ):
        utils.clear_credentials()
        if client.ctx.credentials:
            utils.save_credentials(client.ctx.credentials)

        selected_instance: Optional[str] = preferred_instance
        if not selected_instance:
            # Autoselect an instance, but provide some awareness
            # of the result
            server_info = client.get_server_info()
            selected_instance = server_info.default_yamcs_instance
            if selected_instance:
                eprint(
                    "Using instance:",
                    selected_instance,
                    "(change with: yamcs config set instance xyz)",
                )
            else:
                eprint("No instance")

        if not config.has_section("core"):
            config.add_section("core")
        config.set("core", "url", client.ctx.url)

        if selected_instance:
            config.set("core", "instance", selected_instance)
        else:
            config.remove_option("core", "instance")
        utils.save_config(config)
