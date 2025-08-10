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
