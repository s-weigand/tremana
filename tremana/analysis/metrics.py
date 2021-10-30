"""Module containing metrics to be calculated on tremor accelerometry data or their FFT."""

import numpy as np
import pandas as pd


def center_of_mass(fft_spectra: pd.DataFrame) -> pd.DataFrame:
    r"""Calculate the center of mass of FFT spectra.

    .. math::

        H_{cm} = \dfrac{1}{N-1} \dfrac{\sum\limits_{i=1}^{N}((i-1)X_i)}{\sum\limits_{i=1}^{N}X_i}

    Parameters
    ----------
    fft_spectra : pd.DataFrame
        Dataframe with each column being a FFT spectrum.

    Returns
    -------
    pd.DataFrame
        Dataframe with the center of mass in the with columns names same as the spectra.
    """
    results = {}
    N = fft_spectra.shape[0]
    weights = np.arange(0, N)
    for column in fft_spectra.columns:
        sorted_spectrum = fft_spectra[column].sort_values(ascending=False)
        results[column] = 1 / (N - 1) * sorted_spectrum.dot(weights).sum() / sorted_spectrum.sum()

    return pd.DataFrame(results, index=["H_cm"])
