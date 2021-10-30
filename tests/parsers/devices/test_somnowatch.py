"""Testmodule for the somowatch parser"""
import re
from datetime import datetime
from textwrap import dedent
from typing import Union

import pytest

from tremana.parsers.devices.somnowatch import SOMNOWATCH_TYPE_MAPPING
from tremana.parsers.devices.somnowatch import _somnowatch_parse_header
from tremana.warnings import TremanaParsingIgnoredSignalTypeWarning


def dummy_header(
    *,
    signal_type: str,
    sample_rate: Union[int, float],
    length: int,
    unit: str = "",
):
    formatted_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    header = dedent(
        f"""\
        Signal Type: {signal_type}
        Start Time: {formatted_datetime}
        Sample Rate: {sample_rate}
        Length: {length}
        Unit: {unit}

        Data:
        00:00:00,000; 1

        """
    )

    if signal_type in SOMNOWATCH_TYPE_MAPPING:
        signal_type = SOMNOWATCH_TYPE_MAPPING[signal_type]

    expected = [
        signal_type,
        formatted_datetime,
        float(sample_rate),
        length,
        unit,
    ]

    return header.splitlines(), expected


@pytest.mark.parametrize("signal_type", tuple(SOMNOWATCH_TYPE_MAPPING.keys()))
@pytest.mark.parametrize("sample_rate", (128, 0.033))
@pytest.mark.parametrize("length", (1, 2))
@pytest.mark.parametrize("unit", ("mg", "lm"))
def test_somnowatch_parse_header(signal_type, sample_rate, length, unit):
    header_lines, expected = dummy_header(
        signal_type=signal_type,
        sample_rate=sample_rate,
        length=length,
        unit=unit,
    )
    result = _somnowatch_parse_header(header_lines)
    for result_item, expected_item in zip(result, expected):
        assert result_item == expected_item


@pytest.mark.parametrize("origin_file", (None, "foo_file.txt"))
def test_somnowatch_parse_header_unsupported_signal_type(origin_file):
    header_lines, expected = dummy_header(
        signal_type="foo_signal",
        sample_rate=128,
        length=1,
        unit="unit",
    )
    match_str = "foo_signal"
    if origin_file:
        match_str = re.compile("foo_signal.+foo_file.txt", re.DOTALL)
    with pytest.warns(TremanaParsingIgnoredSignalTypeWarning, match=match_str):
        result = _somnowatch_parse_header(header_lines, origin_file=origin_file)
    for result_item, expected_item in zip(result, expected):
        assert result_item == expected_item
