from pathlib import Path
from textwrap import dedent
from warnings import warn

import pytest

from tremana.warnings import TremanaBaseWarning
from tremana.warnings import TremanaNotSupportedWarning
from tremana.warnings import TremanaSupressableWarning
from tremana.warnings import filter_tremana_warnings


def test_filter_tremana_warnings():
    with pytest.warns(UserWarning, match="not a tremana warning"):
        with filter_tremana_warnings((TremanaNotSupportedWarning, TremanaSupressableWarning)):
            warn(UserWarning("not a tremana warning"))
            warn(TremanaNotSupportedWarning(msg="do not trigger"))
            warn(TremanaSupressableWarning(msg="do not trigger"))

    with pytest.warns(TremanaNotSupportedWarning, match="Legit warning"):
        warn(TremanaNotSupportedWarning(msg="Legit warning"))


def test_TremanaBaseWarning_only_msg():
    with pytest.raises(
        TremanaBaseWarning,
        match="TestRaise",
    ):
        raise TremanaBaseWarning(msg="TestRaise")


def test_TremanaBaseWarning_append_msg():
    with pytest.raises(
        TremanaBaseWarning,
        match="TestRaise\n\nAppended",
    ):
        raise TremanaBaseWarning(msg="TestRaise", append_msg="Appended")


@pytest.mark.parametrize("origin_file_factory", ((str, Path)))
def test_TremanaBaseWarning_origin_file(origin_file_factory):
    with pytest.raises(
        TremanaBaseWarning,
        match=dedent(
            """\
            TestRaise

            This warning was caused processing:
                foo\\.txt

            Appended"""
        ),
    ):
        raise TremanaBaseWarning(
            msg="TestRaise", append_msg="Appended", origin_file=origin_file_factory("foo.txt")
        )


def test_TremanaSupressableWarning():
    with pytest.raises(
        TremanaBaseWarning,
        match=dedent(
            """\
            TestRaise

            If you want to suppress this warning please consult the documentation\\."""
        ),
    ):
        raise TremanaSupressableWarning(msg="TestRaise")


def test_TremanaSupressableWarning_append_msg():
    with pytest.raises(
        TremanaBaseWarning,
        match=dedent(
            """\
            TestRaise

            Appended

            If you want to suppress this warning please consult the documentation\\."""
        ),
    ):
        raise TremanaSupressableWarning(msg="TestRaise", append_msg="Appended")
