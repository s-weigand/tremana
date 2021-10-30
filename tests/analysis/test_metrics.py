import numpy as np
import pandas as pd

from tremana.analysis.metrics import center_of_mass


def test_center_of_mass():
    """Extreme cases described in Edwards1999"""
    single_frequency_fft_data = np.zeros(1000)
    single_frequency_fft_data[5] = 1
    white_noise_fft_data = np.ones(1000)

    fft_data = pd.DataFrame(
        {
            "single_frequency_fft": single_frequency_fft_data,
            "white_noise_fft": white_noise_fft_data,
        }
    )

    result = center_of_mass(fft_data)

    assert result.loc["H_cm", "single_frequency_fft"] == 0
    assert np.allclose(result.loc["H_cm", "white_noise_fft"], 0.5)
