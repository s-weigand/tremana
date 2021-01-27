"""Custom exceptions for tremana."""

from tremana import __repo_short_url__


class TremanaException(Exception):
    """BaseException for expected possible errors with tremana."""

    def __init__(self, msg: str = "", *args: object) -> None:  # noqa: D107
        append_msg = f"If you encounter a bug please open an issue at {__repo_short_url__}."
        super().__init__(f"{msg}\n\n{append_msg}", *args)
