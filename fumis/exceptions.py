"""Exceptions for the Fumis WiRCU API."""


class FumisError(Exception):
    """Generic Fumis exception."""

    pass


class FumisConnectionError(FumisError):
    """Fumis connection exception."""

    pass
