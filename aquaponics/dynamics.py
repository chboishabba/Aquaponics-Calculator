"""Simple system dynamics models."""
from __future__ import annotations

import math

def cstr_concentration(initial_conc: float, inflow_conc: float, flow_rate: float,
                       volume: float, time: float) -> float:
    """Concentration in a continuously stirred tank reactor.

    Parameters
    ----------
    initial_conc: float
        Initial concentration in the tank.
    inflow_conc: float
        Concentration of inflow water.
    flow_rate: float
        Inflow rate (same units as volume per unit time).
    volume: float
        Tank volume.
    time: float
        Time since start.
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    k = flow_rate / volume
    return inflow_conc + (initial_conc - inflow_conc) * math.exp(-k * time)
