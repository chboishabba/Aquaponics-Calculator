"""Alert calculation utilities.

This module provides helpers to derive warning thresholds for a measured
parameter. The function checks the input configuration for obvious
mistakes and raises :class:`ValueError` with a descriptive message when
invalid values are supplied.
"""

from __future__ import annotations


def calculate_warn_range(min_value: float, max_value: float, warn_pct: float):
    """Compute the warning range between ``min_value`` and ``max_value``.

    Parameters
    ----------
    min_value:
        The minimum acceptable value for the reading.
    max_value:
        The maximum acceptable value for the reading. Must be greater
        than ``min_value``.
    warn_pct:
        Fraction of the span between ``min_value`` and ``max_value``
        used to determine the width of the warning bands. Must satisfy
        ``0 <= warn_pct < 0.5``.

    Returns
    -------
    tuple[float, float]
        The lower and upper warning thresholds.

    Raises
    ------
    ValueError
        If ``warn_pct`` or the value range are invalid.
    """
    if not (0 <= warn_pct < 0.5):
        raise ValueError("warn_pct must satisfy 0 <= warn_pct < 0.5")
    if max_value <= min_value:
        raise ValueError("max_value must be greater than min_value")

    span = max_value - min_value
    margin = span * warn_pct
    warn_low = min_value + margin
    warn_high = max_value - margin
    return warn_low, warn_high
