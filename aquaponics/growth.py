"""Fish growth models."""
from __future__ import annotations

def tgc_growth(initial_weight_g: float, tgc: float, temp_sum: float) -> float:
    """Forecast final weight (g) using Thermal Growth Coefficient.

    Parameters
    ----------
    initial_weight_g: float
        Starting fish weight in grams.
    tgc: float
        Thermal Growth Coefficient (per degree-day).
    temp_sum: float
        Cumulative temperature above maintenance (degree-days).
    """
    w13 = initial_weight_g ** (1.0 / 3.0)
    final_w13 = w13 + tgc * temp_sum / 1000.0
    return final_w13 ** 3
