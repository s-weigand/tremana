"""Custom exceptions for tremana."""
import os
from typing import Union

from tremana import __repo_short_url__


class TremanaException(Exception):
    """BaseException for expected possible errors with tremana."""

    def __init__(self, *args: object, msg: str) -> None:  # noqa: D205, D400
        """
        Parameters
        ----------
        msg : str
            Message to be printed.


        .. # noqa: DAR101
        """
        append_msg = f"If you encounter a bug please open an issue at {__repo_short_url__}."
        super().__init__(f"{msg}\n\n{append_msg}", *args)


class TremanaParsingException(TremanaException):
    """Baseclass for parsing Exceptions."""

    def __init__(
        self,
        *args: object,
        msg: str,
        origin_file: Union[str, os.PathLike] = None,
    ) -> None:  # noqa: D205, D400
        """
        Parameters
        ----------
        msg : str
            Message to be printed.
        origin_file : Union[str, os.PathLike]
            Path to the file causing the warning, by default None


        .. # noqa: DAR101
        """
        if origin_file:
            msg = f"{msg}\n\nThis Error was caused processing:\n    {str(origin_file)}"
        super().__init__(*args, msg=msg)


class TremanaParsingSampleRateException(TremanaParsingException):
    """Error thrown when the samplerate can't be parsed to a numerical value."""

    def __init__(
        self,
        *args: object,
        sample_rate: str,
        origin_file: Union[str, os.PathLike] = None,
    ) -> None:  # noqa: D205, D400
        """
        Parameters
        ----------
        sample_rate : str
            Value of the sample rate which should have been cast to float.
        origin_file : Union[str, os.PathLike]
            Path to the file causing the warning, by default None


        .. # noqa: DAR101
        """
        msg = (
            f"Sample rate of value {sample_rate!r} "
            "can't be cast to float, which is needed for fft."
        )
        super().__init__(*args, msg=msg, origin_file=origin_file)
