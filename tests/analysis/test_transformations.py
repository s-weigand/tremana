from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tremana.analysis.transformations import fft_spectra
from tremana.analysis.transformations import power_density_spectra


@pytest.mark.parametrize("time", (30, 60, 120))
@pytest.mark.parametrize(
    "frequencies, amplitudes",
    (
        ((1,), (1,)),
        ((1, 2), (2, 1)),
        ((1, 5, 10), (1, 5, 10)),
    ),
)
@pytest.mark.parametrize("sampling_rate", (1000, 2000))
def test_fft_spectra(
    time: int,
    frequencies: tuple[int | float, ...],
    amplitudes: tuple[int | float, ...],
    sampling_rate: int,
):
    """FFT peaks are at frequency and have amplitude height"""
    t = np.linspace(0, time, num=time * sampling_rate) * 2 * np.pi
    signal_values = np.zeros(t.shape)
    for frequency, amplitude in zip(frequencies, amplitudes):
        signal_values += amplitude * np.sin(frequency * t)
    signal = pd.DataFrame({"X": signal_values}, index=t)

    result = fft_spectra(signal, columns=["X"], sampling_rate=sampling_rate)

    for frequency, amplitude in zip(frequencies, amplitudes):
        fft_amplitude_at_frequency = result["X"].iat[
            result.index.get_loc(frequency, method="nearest")
        ]

        assert np.allclose(fft_amplitude_at_frequency, amplitude, rtol=1e-3)


def test_fft_spectra_normalized():
    """FFT amplitude is set to 1 and columns are used if not provided"""
    time = 30
    sampling_rate = 100
    t = np.linspace(0, time, num=time * sampling_rate) * 2 * np.pi
    frequency = 3
    signal_values = 100 * np.sin(frequency * t)
    signal = pd.DataFrame({"X": signal_values}, index=t)
    result = fft_spectra(signal, sampling_rate=sampling_rate, norm=True)
    fft_amplitude_at_frequency = result["X"].iat[result.index.get_loc(frequency, method="nearest")]

    assert np.allclose(fft_amplitude_at_frequency, 1)


@pytest.mark.parametrize("time", (30, 60, 120))
@pytest.mark.parametrize(
    "frequencies, amplitudes",
    (
        ((1,), (1,)),
        ((1, 2), (2, 1)),
        ((1, 5, 10), (1, 5, 10)),
    ),
)
@pytest.mark.parametrize("sampling_rate", (1000, 2000))
def test_power_density_spectra(
    time: int,
    frequencies: tuple[int | float, ...],
    amplitudes: tuple[int | float, ...],
    sampling_rate: int,
):
    """PDS peaks are at frequency and have amplitude height"""
    t = np.linspace(0, time, num=time * sampling_rate) * 2 * np.pi
    signal_values = np.zeros(t.shape)
    for frequency, amplitude in zip(frequencies, amplitudes):
        signal_values += amplitude * np.sin(frequency * t)
    signal = pd.DataFrame({"X": signal_values}, index=t)

    result = power_density_spectra(signal, columns=["X"], sampling_rate=sampling_rate)

    for frequency, amplitude in zip(frequencies, amplitudes):
        pds_amplitude_at_frequency = result["X"].iat[
            result.index.get_loc(frequency, method="nearest")
        ]

        assert np.allclose(pds_amplitude_at_frequency, amplitude ** 2, rtol=1e-3)


def test_power_density_spectra_normalized():
    """PDS amplitude is set to 1 and columns are used if not provided"""
    time = 30
    sampling_rate = 100
    t = np.linspace(0, time, num=time * sampling_rate) * 2 * np.pi
    frequency = 3
    signal_values = 100 * np.sin(frequency * t)
    signal = pd.DataFrame({"X": signal_values}, index=t)
    result = power_density_spectra(signal, sampling_rate=sampling_rate, norm=True)
    pds_amplitude_at_frequency = result["X"].iat[result.index.get_loc(frequency, method="nearest")]

    assert np.allclose(pds_amplitude_at_frequency, 1)
