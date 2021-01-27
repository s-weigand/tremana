import pytest

from tremana.exceptions import TremanaException


def test_TremanaException():
    with pytest.raises(
        TremanaException,
        match=r"Foo\n\nIf you encounter a bug please open an issue at https://git\.io/JtCN6\.",
    ):
        raise TremanaException("Foo")
