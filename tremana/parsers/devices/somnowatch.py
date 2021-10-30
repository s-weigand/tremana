"""Module containing the somowatch parser.

See: https://somnomedics.de
"""
from __future__ import annotations

import os
from typing import Iterable
from typing import NamedTuple
from warnings import warn

import numpy as np
import pandas as pd

from tremana.exceptions import TremanaParsingSampleRateException
from tremana.utils.dataframe_helper import extract_position_by_value
from tremana.utils.io import lazy_read_headers
from tremana.warnings import TremanaParsingIgnoredSignalTypeWarning
from tremana.warnings import TremanaParsingInconsistentMetadataWarning
from tremana.warnings import filter_tremana_warnings

SOMNOWATCH_TYPE_MAPPING = {
    "X_AC_Type": "X",
    "Y_AC_Type": "Y",
    "Z_AC_Type": "Z",
    "Mag_Type": "Mag",
}


class SomnoWatchMetaData(NamedTuple):
    """NamedTuple representing the somnowatch meta information."""

    signal_type: str
    start_date: str
    sample_rate: float
    length: int
    unit: str


def _somnowatch_parse_header(
    header_lines: list[str],
    origin_file: None | str | os.PathLike[str] = None,
) -> SomnoWatchMetaData:
    """Parser for the header information of somnowatch files.

    Parameters
    ----------
    header_lines: List[str]
        List of lines containing the full header of an exported
        somnowatch measurement file.
    origin_file : str | os.PathLike[str], optional
        Path to the file causing the warning, by default None

    Returns
    -------
    SomnoWatchMetaData
        Metadata describing the measurement

    Warns
    -----
    TrenanaParsingIgnoredSignalTypeWarning
        If type signal type isn't supported

    Raises
    ------
    TremanaParsingSampleRateException
        If sample_rate can't be parsed to a float

    See Also
    --------
    SomnoWatchMetaData


    .. # noqa: DAR401 TremanaParsingSampleRateException
    .. # noqa: DAR402 TrenanaParsingIgnoredSignalTypeWarning
    """
    header_vals = [line.split(":", 1)[-1].strip() for line in header_lines[:5]]
    try:
        signal_type = SOMNOWATCH_TYPE_MAPPING[header_vals[0]]
    except KeyError:
        signal_type = header_vals[0]
        warn(
            TremanaParsingIgnoredSignalTypeWarning(
                signal_type=signal_type, origin_file=origin_file
            )
        )
    start_date = header_vals[1]
    try:
        sample_rate = float(header_vals[2])
    except ValueError:
        raise TremanaParsingSampleRateException(
            sample_rate=header_vals[2], origin_file=origin_file
        )
    length = int(header_vals[3])
    unit = header_vals[4]
    return SomnoWatchMetaData(signal_type, start_date, sample_rate, length, unit)


def _somnowatch_validate_meta_data(
    file_paths: Iterable[str | os.PathLike[str]],
    ignore_signal_types: list[str] = ["Light_Type", "Accu_Type"],
) -> pd.DataFrame:
    header_lines_list = lazy_read_headers(file_paths, lines_to_read=5)
    ignore_regex = f"'({'|'.join(ignore_signal_types)})'"
    with filter_tremana_warnings((TremanaParsingIgnoredSignalTypeWarning,), message=ignore_regex):
        metadata_df = pd.DataFrame(
            [
                _somnowatch_parse_header(header_lines=header_lines, origin_file=origin_file)
                for header_lines, origin_file in zip(header_lines_list, file_paths)
            ],
            index=list(map(str, file_paths)),
        )

    metadata_df.drop(columns=ignore_signal_types, inplace=True, errors="ignore")
    metadata_df["start_date"] = pd.to_datetime(metadata_df["start_date"])
    metadata_df = metadata_df[~metadata_df["signal_type"].isin(ignore_signal_types)]
    most_common: pd.Series = metadata_df.mode().iloc[0, :]

    all_equal_metadata_mask: pd.DataFrame = metadata_df == most_common
    # signal_type is supposed to differ
    all_equal_metadata_mask.drop(columns=["signal_type"], inplace=True)

    if not np.all(all_equal_metadata_mask):
        positions: list[tuple[str, str]] = extract_position_by_value(  # type:ignore
            all_equal_metadata_mask, value=False
        )
        for file_path, value_name in positions:
            if metadata_df.loc[file_path, "signal_type"] not in ignore_signal_types:
                value: str | float | int = metadata_df.at[file_path, value_name]
                expected_value: str | float | int = most_common[value_name]
                warn(
                    TremanaParsingInconsistentMetadataWarning(
                        actual_value=value,
                        expected_value=expected_value,
                        metadata_name=value_name,
                        origin_file=file_path,
                    )
                )

    return metadata_df


def _somnowatch_validate_measurement_data(
    file_paths: Iterable[str | os.PathLike[str]],
    ignore_signal_types: list[str] = ["Light_Type", "Accu_Type"],
) -> None:
    metadata_df = _somnowatch_validate_meta_data(
        file_paths=file_paths, ignore_signal_types=ignore_signal_types
    )
    data_frames = []
    for file in file_paths:
        metadata_row = metadata_df[str(file)]
        signal_type = metadata_row["signal_type"].squeeze()
        unit = metadata_row["unit"].squeeze()
        data_frames.append(
            pd.read_csv(
                file,
                skiprows=7,
                decimal=",",
                sep=";",
                names=["time", f"{signal_type} amplitude in {unit}"],
                parse_dates=["time"],
            )
        )
