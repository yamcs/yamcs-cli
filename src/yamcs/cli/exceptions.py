class YamcsCLIError(Exception):
    """Base class for raised exceptions."""


class NoServerError(YamcsCLIError):
    """No Yamcs server is configured."""


class NoInstanceError(YamcsCLIError):
    """No Yamcs instance is configured."""
