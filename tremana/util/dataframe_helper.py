"""Helper functions to extract information from DataFrames."""
from __future__ import annotations

import numpy as np
import pandas as pd


def extract_position_by_value(df: pd.DataFrame, value: object) -> list[tuple[object, object]]:
    """Extract index and column where the dataframe has the value ``value``.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe the columns and indices should be extracted from.
    value : object
        Value to look for in ``df``

    Returns
    -------
    list[tuple[object, object]]
        List of indices and column where ``df`` has the value ``value``
    """
    # This is needed since True==1, because bool is a subclass of int
    if isinstance(value, bool):
        filter_df: pd.DataFrame = df.loc[:, df.dtypes == bool]
    else:
        filter_df = df.loc[:, df.dtypes != bool]
    return [
        (filter_df.index[index], filter_df.columns[column])
        for index, column in np.argwhere((filter_df == value).values)
    ]
