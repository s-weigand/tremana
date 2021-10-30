from datetime import datetime

import pandas as pd
import pytest

from tremana.utils.dataframe_helper import extract_position_by_value


@pytest.mark.parametrize(
    "value, expected",
    (
        (1, [("foo1", "int_val")]),
        (True, [("foo1", "bool_val"), ("foo3", "bool_val")]),
        ("foo", [("foo1", "str_val")]),
        (datetime(1970, 1, 2), [("foo2", "date_val")]),
    ),
)
def test_extract_position_by_value(value, expected):
    df = pd.DataFrame(
        {
            "int_val": [1, 2, 3],
            "bool_val": [True, False, True],
            "str_val": ["foo", "bar", "baz"],
            "date_val": [datetime(1970, 1, 1), datetime(1970, 1, 2), datetime(1970, 1, 3)],
        },
        index=["foo1", "foo2", "foo3"],
    )

    assert extract_position_by_value(df, value) == expected
