"""Fish growth models."""
from __future__ import annotations

def tgc_growth(initial_weight_g: float, tgc: float, temp_sum: float) -> float:
    """Forecast final weight (g) using Thermal Growth Coefficient.

    Parameters
    ----------
    initial_weight_g: float
        Starting fish weight in grams. Must be non-negative.
    tgc: float
        Thermal Growth Coefficient (per degree-day). Must be non-negative.
    temp_sum: float
        Cumulative temperature above maintenance (degree-days). Must be non-negative.
    """
    if initial_weight_g < 0:
        raise ValueError("initial_weight_g must be non-negative")
    if tgc < 0:
        raise ValueError("tgc must be non-negative")
    if temp_sum < 0:
        raise ValueError("temp_sum must be non-negative")
    w13 = initial_weight_g ** (1.0 / 3.0)
    final_w13 = w13 + tgc * temp_sum / 1000.0
    return final_w13 ** 3
