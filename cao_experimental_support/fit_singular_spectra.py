"""Compare exponential and power-law fits to raw and centered SVD spectra.

In a notebook, place this file beside the notebook and run:
    from fit_singular_spectra import fit_spectra
    fig, results = fit_spectra(sigma_raw, sigma_centered, n_fit=10)
    print(results.to_string(index=False))
    plt.show()

Fits minimize squared residuals of normalized singular values on their original
scale (not log-transformed values). Both models have two free parameters and
use identical mode indices. No additive offset is fitted. RMSE and R-squared
are descriptive fit statistics, not significance tests or proof of a mechanism.
The first 10 modes are a plotting default, not an estimated signal/noise cutoff.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exponential(k, amplitude, decay):
    return amplitude * np.exp(-decay * (k - 1))


def power_law(k, amplitude, exponent):
    return amplitude * np.power(k, -exponent)


def _check_spectrum(values, name):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size < 4:
        raise ValueError(f"{name} must be a one-dimensional spectrum of length >= 4.")
    if not np.all(np.isfinite(values)) or np.any(values < 0) or values[0] <= 0:
        raise ValueError(f"{name} must be finite and nonnegative with a positive first value.")
    if np.any(np.diff(values) > 1e-12 * values[0]):
        raise ValueError(f"{name} must be sorted in descending order, as returned by svdvals.")
    return values


def fit_spectra(sigma_raw, sigma_centered, n_fit=10):
    """Return a Matplotlib figure and four-row pandas table of descriptive fits.

    n_fit: number of leading modes to fit, or None for all available shared
        modes. Choose this independently of which model has the smaller error.
    A single terminal numerical zero is removed from the centered spectrum.
    That removal does not estimate or remove the experimental noise floor.
    """
    raw = _check_spectrum(sigma_raw, "sigma_raw")
    centered = _check_spectrum(sigma_centered, "sigma_centered")
    # The user's neuron-by-time matrix has more neurons than time bins.
    # Row centering imposes a constant temporal null direction. Only discard
    # one terminal value, and only if it is numerically indistinguishable from 0.
    tolerance = np.finfo(float).eps * max(raw.size, centered.size) * centered[0]
    if centered[-1] <= tolerance:
        centered = centered[:-1]

    available = min(raw.size, centered.size)
    if n_fit is None:
        n_fit = available
    elif isinstance(n_fit, bool) or not isinstance(n_fit, (int, np.integer)):
        raise ValueError("n_fit must be an integer or None.")
    if not 4 <= n_fit <= available:
        raise ValueError(f"n_fit must be between 4 and {available}.")

    k = np.arange(1, n_fit + 1, dtype=float)
    k_dense = np.linspace(1, n_fit, 400)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True,
                             constrained_layout=True)
    rows = []
    for ax, title, spectrum in zip(
        axes, ["Including mean firing", "Temporal mean subtracted"], [raw, centered]
    ):
        y = spectrum[:n_fit] / spectrum[0]
        ax.plot(k, y, "o", color="black", markersize=4, label="Observed spectrum")
        for name, model, color, style in [
            ("Exponential", exponential, "tab:blue", "-"),
            ("Power law", power_law, "tab:orange", "--"),
        ]:
            # Try several starting exponents to reduce optimizer sensitivity.
            candidates = []
            for initial_exponent in (0.05, 0.5, 1.0, 2.0, 5.0):
                try:
                    params, _ = curve_fit(
                        model, k, y, p0=(1.0, initial_exponent),
                        bounds=([0.0, 0.0], [np.inf, np.inf]),
                        maxfev=20000, ftol=1e-12, xtol=1e-12, gtol=1e-12,
                    )
                except RuntimeError:
                    continue
                sse = float(np.sum((y - model(k, *params)) ** 2))
                candidates.append((sse, params))
            if not candidates:
                raise RuntimeError(f"All {name} fits failed for {title}.")
            sse, params = min(candidates, key=lambda item: item[0])
            sst = float(np.sum((y - y.mean()) ** 2))
            r_squared = 1 - sse / sst if sst > 0 else np.nan
            rows.append({
                "Spectrum": title, "Model": name, "Modes": n_fit,
                "A": params[0], "Decay_or_exponent": params[1],
                "RMSE": np.sqrt(sse / n_fit), "R_squared": r_squared,
            })
            ax.plot(k_dense, model(k_dense, *params), style, color=color,
                    label=f"{name} ($R^2$={r_squared:.3f})")
        ax.set(title=title, xlabel="Singular-value index k", xlim=(1, n_fit))
        ax.set_ylim(bottom=0)
        ax.set_xscale("linear")
        ax.set_yscale("linear")
        ax.grid(alpha=0.2)
        ax.legend(fontsize=9)
    axes[0].set_ylabel(r"$\sigma_k / \sigma_1$")
    fig.suptitle(f"Original-scale least-squares fits: first {n_fit} modes")
    return fig, pd.DataFrame(rows)
