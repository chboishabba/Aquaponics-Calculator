"""Filtering utilities for sensor data."""
from __future__ import annotations

from typing import Iterable, List
import statistics as stats


def hampel_filter(data: Iterable[float], window_size: int = 5, n_sigmas: float = 3.0) -> List[float]:
    """Apply a Hampel filter for outlier removal using pure Python.

    Parameters
    ----------
    data : Iterable[float]
        Sequence of values to filter.
    window_size : int, optional
        Size of the centered sliding window. Must be greater than ``0``.
    n_sigmas : float, optional
        Threshold in scaled median absolute deviations. Must be greater than
        ``0``.

    Returns
    -------
    List[float]
        Filtered values with outliers replaced by the window median.

    Raises
    ------
    ValueError
        If ``window_size`` or ``n_sigmas`` are not greater than ``0``.
    """
    if window_size <= 0:
        raise ValueError("window_size must be > 0")
    if n_sigmas <= 0:
        raise ValueError("n_sigmas must be > 0")
    x = list(map(float, data))
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if n_sigmas <= 0:
        raise ValueError("n_sigmas must be positive")
    if not x:
        return []
    if len(x) < 2 * window_size + 1:
        raise ValueError("window_size too large for data length")
    k = window_size
    new_x = x[:]
    for i in range(k, len(x) - k):
        window = x[i - k : i + k + 1]
        median = stats.median(window)
        mad = stats.median([abs(v - median) for v in window])
        if mad == 0:
            if x[i] != median:
                new_x[i] = median
            continue
        if abs(x[i] - median) > n_sigmas * 1.4826 * mad:
            new_x[i] = median
    return new_x


def ewma(data: Iterable[float], alpha: float) -> List[float]:
    """Compute an exponentially weighted moving average.

    Parameters
    ----------
    data : Iterable[float]
        Sequence of values to smooth.
    alpha : float
        Smoothing factor. Must satisfy ``0 < alpha <= 1``.

    Returns
    -------
    List[float]
        Smoothed values.

    Raises
    ------
    ValueError
        If ``alpha`` is not within ``(0, 1]``.
    """
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    x = list(map(float, data))
    if not (0 < alpha <= 1):
        raise ValueError("alpha must satisfy 0 < alpha <= 1")
    if not x:
        return []
    ewma_vals = [x[0]]
    for value in x[1:]:
        ewma_vals.append(alpha * value + (1 - alpha) * ewma_vals[-1])
    return ewma_vals
