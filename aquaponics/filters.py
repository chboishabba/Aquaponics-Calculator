"""Filtering utilities for sensor data."""
from __future__ import annotations

from typing import Iterable, List
import statistics as stats


def hampel_filter(data: Iterable[float], window_size: int = 5, n_sigmas: float = 3.0) -> List[float]:
    """Apply a Hampel filter for outlier removal using pure Python."""
    x = list(map(float, data))
    if not x:
        return []
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
    """Compute an exponentially weighted moving average."""
    x = list(map(float, data))
    if not x:
        return []
    ewma_vals = [x[0]]
    for value in x[1:]:
        ewma_vals.append(alpha * value + (1 - alpha) * ewma_vals[-1])
    return ewma_vals
