"""Water quality calculations."""
from __future__ import annotations

import math


def nh3_fraction(pH: float, temp_c: float) -> float:
    """Fraction of unionized ammonia (NH3) in Total Ammonia Nitrogen.

    Based on the freshwater formulation of Emerson et al. (1975).

    Parameters
    ----------
    pH: float
        Water pH.
    temp_c: float
        Water temperature in Celsius. Must be non-negative.
    """
    if temp_c < 0:
        raise ValueError("temp_c must be non-negative")
    temp_k = temp_c + 273.15
    pka = 0.09018 + 2729.92 / temp_k
    return 1.0 / (1 + 10 ** (pka - pH))

def do_saturation(temp_c: float) -> float:
    """Dissolved oxygen saturation concentration in mg/L for freshwater.

    Uses the Weiss (1970) equation for zero salinity at sea level.

    Parameters
    ----------
    temp_c: float
        Water temperature in Celsius. Must be non-negative.
    """
    if temp_c < 0:
        raise ValueError("temp_c must be non-negative")
    temp_k = temp_c + 273.15
    ln_do = (-139.34411
             + 1.575701e5 / temp_k
             - 6.642308e7 / temp_k**2
             + 1.243800e10 / temp_k**3
             - 8.621949e11 / temp_k**4)
    return math.exp(ln_do)

def tan_capacity_q10(surface_area_m2: float, base_rate: float, temp_c: float,
                     ref_temp_c: float = 20.0, q10: float = 1.5) -> float:
    """Compute nitrification capacity (g TAN/day) with Q10 correction.

    Parameters
    ----------
    surface_area_m2: float
        Biofilter surface area. Must be non-negative.
    base_rate: float
        Reference nitrification rate (g TAN/m^2/day) at ref_temp_c. Must be non-negative.
    temp_c: float
        Current water temperature. Must be non-negative.
    ref_temp_c: float
        Reference temperature for base_rate. Must be non-negative.
    q10: float
        Temperature coefficient.
    """
    if surface_area_m2 < 0:
        raise ValueError("surface_area_m2 must be non-negative")
    if base_rate < 0:
        raise ValueError("base_rate must be non-negative")
    if temp_c < 0:
        raise ValueError("temp_c must be non-negative")
    if ref_temp_c < 0:
        raise ValueError("ref_temp_c must be non-negative")
    rate = base_rate * q10 ** ((temp_c - ref_temp_c) / 10.0)
    return surface_area_m2 * rate
