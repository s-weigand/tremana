"""Custom Warnings for tremana."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any
from typing import Generator
from typing import Iterable
from warnings import catch_warnings
from warnings import filterwarnings

from tremana import __repo_short_url__


class TremanaBaseWarning(UserWarning):
    """Basewarning for expected possible errors with tremana."""

    def __init__(
        self,
        *args: object,
        msg: str,
        origin_file: str | os.PathLike[str] | None = None,
        append_msg: str | None = None,
    ) -> None:  # noqa: D205, D400
        """

        Parameters
        ----------
        msg : str
            Message to be printed.
        origin_file : Union[str, os.PathLike], optional
            Path to the file causing the warning, by default None
        append_msg : Optional[str], optional
            Message to be appended on ``msg``, by default None


        .. # noqa: DAR101
        """
        if origin_file:
            msg = f"{msg}\n\nThis warning was caused processing:\n    {str(origin_file)}"
        if append_msg:
            msg = f"{msg}\n\n{append_msg}"
        super().__init__(f"{msg}", *args)


@contextmanager
def filter_tremana_warnings(
    warning_types: Iterable[type[TremanaBaseWarning]], message: str = ""
) -> Generator[None, None, None]:
    """Contextmanager to filter all warnings defined in ``warning_types``.

    Parameters
    ----------
    warning_types : Iterable[Type[TremanaBaseWarning]]
        Warnings to be filtered
    message : str
        Regular expression to filter warnings by.


    .. # noqa: DAR301
    .. # noqa: DAR101
    """
    with catch_warnings():
        for warning in warning_types:
            filterwarnings("ignore", category=warning, message=f".+{message}")
        yield


class TremanaSupressableWarning(TremanaBaseWarning):
    """Basewarning for supressable warnings.

    This baseclass can be used to conveniently suppress all none critical warnings.

    See Also
    --------
    filter_tremana_warnings
    """

    def __init__(
        self,
        *args: object,
        msg: str,
        append_msg: str | None = None,
        **kwargs: Any,
    ) -> None:  # noqa: D205, D400
        """
        Parameters
        ----------
        msg : str
            Message to be printed.
        append_msg : Optional[str], optional
            Message to be appended on ``msg``, by default None


        .. # noqa: DAR101
        """
        supress_msg = "If you want to suppress this warning please consult the documentation."
        if append_msg:
            supress_msg = f"{append_msg}\n\n{supress_msg}"
        super().__init__(*args, msg=msg, append_msg=supress_msg, **kwargs)


class TremanaNotSupportedWarning(TremanaSupressableWarning):
    """Basewarning for not yet supported features."""

    def __init__(self, *args: object, msg: str, **kwargs: Any) -> None:  # noqa: D205, D400
        """
        Parameters
        ----------
        msg : str
            Message to be printed.


        .. # noqa: DAR101
        """
        append_msg = f"If you needs this feature open a feature request at {__repo_short_url__}."
        super().__init__(*args, msg=msg, append_msg=append_msg, **kwargs)


class TremanaParsingIgnoredSignalTypeWarning(TremanaNotSupportedWarning):
    """Warning for not supported signal types."""

    def __init__(self, *args: object, signal_type: str, **kwargs: Any) -> None:  # noqa: D205, D400
        """

        Parameters
        ----------
        signal_type : str
            Value of the signal type.


        .. # noqa: DAR101
        """
        msg = f"Signals of type {signal_type!r} aren't used by tremana yet and will be ignored."
        super().__init__(*args, msg=msg, **kwargs)


class TremanaParsingInconsistentMetadataWarning(TremanaSupressableWarning):
    """Warning for inconsistent metadata in a measurement."""

    def __init__(
        self,
        *args: object,
        actual_value: Any,
        expected_value: Any,
        metadata_name: str,
        origin_file: str | os.PathLike[str],
        **kwargs: Any,
    ) -> None:  # noqa: D205, D400
        """

        Parameters
        ----------
        actual_value : Any
            Value of the metadata
        expected_value : Any
            Expected value of the metadata
        metadata_name : str
            Name of the metadata
        origin_file : Union[str, os.PathLike]
            Path to the file causing the warning


        .. # noqa: DAR101
        """
        msg = (
            f"The value of the {metadata_name!r} was of value {actual_value!r} "
            f"while other files have the value {expected_value!r}.\n"
            "This could mean that the parts of the measurements don't belong together."
        )
        super().__init__(*args, msg=msg, origin_file=origin_file, **kwargs)


class TremanaParsingIncorrectDateFormatWarning(TremanaSupressableWarning):
    """Warning when date format_str doesn't match date_str."""

    def __init__(
        self, *args: object, date_str: str, format_str: str, **kwargs: Any
    ) -> None:  # noqa: D205, D400
        """

        Parameters
        ----------
        date_str : str
            Value of the string which should be parsed
        format_str : str
            Format string used to parse ``date_str``.


        .. # noqa: DAR101
        """
        msg = (
            f"The date {date_str!r} can't be parsed with the provided "
            f"datetime_format {format_str!r}."
        )
        super().__init__(*args, msg=msg, **kwargs)
