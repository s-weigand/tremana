"""Transformations to be used on tremor accelerometry data (e.g.: FFT)."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from scipy.signal import periodogram


def fft_spectra(
    input_dataframe: pd.DataFrame,
    columns: Iterable[str] | None = None,
    sampling_rate: int | float = 128,
    norm: bool = False,
) -> pd.DataFrame:
    """Calculate the FFT of accelerometry data.

    Parameters
    ----------
    input_dataframe : pd.DataFrame
        Dataframe containing accelerometry data.
    columns : Iterable[str], optional
        Columns co calculate the FFT for,
        by default None which results in all columns to be used
    sampling_rate : int
        Number of sample per second, by default 128
    norm : bool
        Whether to normalize the the data to 1 or not, by default False

    Returns
    -------
    pd.DataFrame
        FFT spectra of the accelerometry data.
    """
    n_samples = input_dataframe.shape[0]
    freq = np.fft.fftfreq(n_samples, d=1 / sampling_rate)
    fft_results = {}
    if columns is None:
        columns = input_dataframe.columns
    for column in columns:
        fft_vals = 2 / n_samples * np.abs(np.fft.fft(input_dataframe[column]))
        if norm:
            fft_vals /= fft_vals.max()
        fft_results[column] = fft_vals
    fft_df = pd.DataFrame(fft_results, index=freq)
    return fft_df.iloc[freq >= 0, :]


def power_density_spectra(
    input_dataframe: pd.DataFrame,
    columns: Iterable[str] | None = None,
    sampling_rate: int | float = 128,
    norm: bool = False,
) -> pd.DataFrame:
    """Calculate the power density spectra of accelerometry data.

    Compared to the FFT the resulting values are FFT[-freq]*FFT[freq] with freq>=0.

    Parameters
    ----------
    input_dataframe : pd.DataFrame
        Dataframe containing accelerometry data.
    columns : Iterable[str]
        Columns co calculate the FFT for,
        by default None which results in all columns to be used
    sampling_rate : int | float
        Number of sample per second, by default 128
    norm : bool
        Whether to normalize the the data to 1 or not, by default False

    Returns
    -------
    pd.DataFrame
        Power density spectra accelerometry data.
    """
    pds_results = {}
    if columns is None:
        columns = input_dataframe.columns
    for column in columns:
        frequency, power_density = periodogram(input_dataframe[column], sampling_rate)
        if norm:
            power_density /= power_density.max()
        else:
            power_density *= 2 / (input_dataframe.shape[0] / sampling_rate)
        pds_results[column] = power_density
    return pd.DataFrame(pds_results, index=frequency)
