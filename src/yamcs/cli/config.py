from yamcs.cli import utils


class ConfigCommand(utils.Command):
    def __init__(self, parent):
        super(ConfigCommand, self).__init__(
            parent, "config", "Manage Yamcs client properties"
        )

        def PropertyCompleter(**kwargs):
            return utils.Command.config_options

        subparsers = self.parser.add_subparsers(title="Commands", metavar="COMMAND")
        subparsers.required = True

        subparser = self.create_subparser(subparsers, "list", "List client properties")
        subparser.set_defaults(func=self.list_)

        get_parser = self.create_subparser(
            subparsers, "get", "Get value of client property"
        )
        get_parser.add_argument(
            "property", metavar="PROPERTY", type=str, help="Property"
        ).completer = PropertyCompleter
        get_parser.set_defaults(func=self.get)

        set_parser = self.create_subparser(subparsers, "set", "Set client property")
        set_parser.add_argument(
            "property", metavar="PROPERTY", type=str, help="Property"
        ).completer = PropertyCompleter
        set_parser.add_argument("value", metavar="VALUE", type=str, help="Value")
        set_parser.set_defaults(func=self.set_)

        unset_parser = self.create_subparser(
            subparsers, "unset", "Unset client property"
        )
        unset_parser.add_argument(
            "property", metavar="PROPERTY", type=str, help="Property"
        ).completer = PropertyCompleter
        unset_parser.set_defaults(func=self.unset)

    def list_(self, args):
        config = utils.read_config()
        for section in config.sections():
            print("[{}]".format(section))
            for k, v in list(config.items(section)):
                print("{} = {}".format(k, v))

    def get(self, args):
        section, key = self.parse_option(args.property)
        config = utils.read_config()
        if config.has_option(section, key):
            print(config.get(section, key))

    def set_(self, args):
        section, key = self.parse_option(args.property)
        config = utils.read_config()
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, args.value)
        utils.save_config(config)

    def unset(self, args):
        section, key = self.parse_option(args.property, strict=False)
        config = utils.read_config()
        if config.has_section(section):
            if config.has_option(section, key):
                config.remove_option(section, key)
            if not config.items(section):
                config.remove_section(section)
        utils.save_config(config)

    def parse_option(self, option, strict=True):
        if (option not in self.config_options) and ("." not in option):
            option = "core." + option

        if strict and (option not in self.config_options):
            raise ValueError(f"*** Unknown option '{option}'")

        return option.rsplit(".", 1)
