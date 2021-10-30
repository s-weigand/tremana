from pathlib import Path
from textwrap import dedent
from warnings import warn

import pytest

from tremana.warnings import TremanaBaseWarning
from tremana.warnings import TremanaNotSupportedWarning
from tremana.warnings import TremanaParsingIgnoredSignalTypeWarning
from tremana.warnings import TremanaParsingInconsistentMetadataWarning
from tremana.warnings import TremanaParsingIncorrectDateFormatWarning
from tremana.warnings import TremanaSupressableWarning
from tremana.warnings import filter_tremana_warnings


def test_filter_tremana_warnings():
    with pytest.warns((UserWarning, TremanaBaseWarning), match="Legit warning") as record:
        with filter_tremana_warnings((TremanaNotSupportedWarning, TremanaSupressableWarning)):
            warn(UserWarning("Legit warning"))
            warn(TremanaNotSupportedWarning(msg="do not trigger"))
            warn(TremanaSupressableWarning(msg="do not trigger"))
            warn(TremanaParsingIgnoredSignalTypeWarning(signal_type="do not trigger"))
    assert len(record) == 1

    with pytest.warns(TremanaParsingIgnoredSignalTypeWarning, match="NOT_IGNORED") as record:
        with filter_tremana_warnings(
            (TremanaNotSupportedWarning,), message="'(IGNORED1|IGNORED2)'"
        ):
            warn(TremanaParsingIgnoredSignalTypeWarning(signal_type="NOT_IGNORED"))
            warn(TremanaParsingIgnoredSignalTypeWarning(signal_type="IGNORED1"))
            warn(TremanaParsingIgnoredSignalTypeWarning(signal_type="IGNORED2"))
    assert len(record) == 1

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


def test_TremanaParsingIgnoredSignalTypeWarning():
    with pytest.raises(
        TremanaParsingIgnoredSignalTypeWarning,
        match=dedent(
            """\
            Signals of type 'NOT_SUPPORTED' aren't used by tremana yet and will be ignored\\.

            If you needs this feature open a feature request at https://git\\.io/JtCN6\\.

            If you want to suppress this warning please consult the documentation\\."""
        ),
    ):
        raise TremanaParsingIgnoredSignalTypeWarning(signal_type="NOT_SUPPORTED")


def test_TremanaParsingInconsistentMetadataWarning():
    with pytest.raises(
        TremanaParsingInconsistentMetadataWarning,
        match=dedent(
            """\
            The value of the 'fake_meta' was of value 'baz' while other files have the value 'bar'\\.
            This could mean that the parts of the measurements don't belong together\\.

            This warning was caused processing:
                foo\\.txt

            If you want to suppress this warning please consult the documentation\\."""  # noqa: E501
        ),
    ):
        raise TremanaParsingInconsistentMetadataWarning(
            actual_value="baz",
            expected_value="bar",
            metadata_name="fake_meta",
            origin_file="foo.txt",
        )


def test_TremanaParsingIncorrectDateFormatWarning():
    with pytest.raises(
        TremanaParsingIncorrectDateFormatWarning,
        match=dedent(
            """\
            The date '01.01.1970 00:00:00' can't be parsed with the provided datetime_format '%Y-%m-%d %H:%M:%S'\\.

            If you want to suppress this warning please consult the documentation\\."""  # noqa: E501
        ),
    ):
        raise TremanaParsingIncorrectDateFormatWarning(
            date_str="01.01.1970 00:00:00", format_str="%Y-%m-%d %H:%M:%S"
        )
