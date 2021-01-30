from pathlib import Path
from textwrap import dedent

import pytest

from tremana.exceptions import TremanaException
from tremana.exceptions import TremanaParsingException
from tremana.exceptions import TremanaParsingSampleRateException


def test_TremanaException():
    with pytest.raises(
        TremanaException,
        match=r"Foo\n\nIf you encounter a bug please open an issue at https://git\.io/JtCN6\.",
    ):
        raise TremanaException(msg="Foo")


def test_TremanaParsingException():
    with pytest.raises(
        TremanaParsingException,
        match=dedent(
            """\
            Foo

            If you encounter a bug please open an issue at https://git\\.io/JtCN6\\."""
        ),
    ):
        raise TremanaParsingException(msg="Foo")


@pytest.mark.parametrize("origin_file_factory", ((str, Path)))
def test_TremanaParsingException_origin_file(origin_file_factory):
    with pytest.raises(
        TremanaParsingException,
        match=dedent(
            """\
            Foo

            This Error was caused processing:
                foo\\.txt

            If you encounter a bug please open an issue at https://git\\.io/JtCN6\\."""
        ),
    ):
        raise TremanaParsingException(msg="Foo", origin_file=origin_file_factory("foo.txt"))


def test_TremanaParsingSampleRateException():
    with pytest.raises(
        TremanaParsingSampleRateException,
        match=dedent(
            """\
            Sample rate of value '1\\.2abc' can't be cast to float, which is needed for fft\\.

            This Error was caused processing:
                foo\\.txt

            If you encounter a bug please open an issue at https://git\\.io/JtCN6\\."""
        ),
    ):
        raise TremanaParsingSampleRateException(sample_rate="1.2abc", origin_file="foo.txt")
