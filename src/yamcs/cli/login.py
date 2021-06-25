from getpass import getpass

from yamcs.cli import utils
from yamcs.client import YamcsClient
from yamcs.core import auth


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

    def do_login(self, args):
        opts = utils.CommandOptions(args)

        url = args.url or self.read_url(opts)

        client_kwargs = {
            **utils._parse_url(url),
            "tls_verify": False,
        }

        # First a simple client without any auth (some paths are unprotected)
        client = YamcsClient(**client_kwargs)

        if args.kerberos:
            try:
                from yamcs.kerberos import KerberosCredentials
            except ImportError:
                print(
                    "*** Missing Kerberos support. This is included in "
                    "the optional package: yamcs-client-kerberos"
                )
                return False

            credentials = KerberosCredentials()
            client = YamcsClient(credentials=credentials, **client_kwargs)
            print("Login succeeded")
        elif client.get_auth_info().require_authentication:
            credentials = self.read_credentials()
            if credentials:
                client = YamcsClient(credentials=credentials, **client_kwargs)
                print("Login succeeded")
        else:
            user_info = client.get_user_info()
            print("Anonymous login succeeded (username: {})".format(user_info.username))

        self.save_client_config(client, opts.config)

    def read_url(self, opts):
        default_url = opts.url or "http://localhost:8090"
        return input("URL [{}]: ".format(default_url)) or default_url

    def read_credentials(self):
        username = input("Username: ")
        if not username:
            print("*** Username may not be empty")
            return False

        password = getpass("Password: ")
        if not password:
            print("*** Password may not be empty")
            return False

        return auth.Credentials(username=username, password=password)

    def save_client_config(self, client, config):
        utils.clear_credentials()
        if client.ctx.credentials:
            utils.save_credentials(client.ctx.credentials)
        server_info = client.get_server_info()

        if not config.has_section("core"):
            config.add_section("core")
        config.set("core", "url", client.ctx.url)

        # Temporary (cleanup old config properties. 'host/port' was migrated to 'url')
        config.remove_option("core", "host")
        config.remove_option("core", "port")

        if server_info.default_yamcs_instance:
            config.set("core", "instance", server_info.default_yamcs_instance)
        else:
            config.remove_option("core", "instance")
        utils.save_config(config)
