"""Basic rule engine for generating alerts."""
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Alert:
    parameter: str
    severity: str
    message: str

def check_threshold(parameter: str, value: float, min_value: float, max_value: float,
                    warn_pct: float = 0.1) -> Alert:
    """Generate an alert based on threshold comparisons."""
    range_span = max_value - min_value
    warn_low = min_value + warn_pct * range_span
    warn_high = max_value - warn_pct * range_span
    if value < min_value or value > max_value:
        severity = "critical"
    elif value <= warn_low or value >= warn_high:
        severity = "warning"
    else:
        severity = "normal"
    msg = (
        f"{parameter}={value:.2f} outside {min_value}-{max_value}"
        if severity == "critical"
        else f"{parameter} approaching limit" if severity == "warning" else f"{parameter} within range"
    )
    return Alert(parameter, severity, msg)

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
