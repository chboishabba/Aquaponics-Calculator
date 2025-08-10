
"""Core algorithms for aquaponics analytics."""

from .filters import hampel_filter, ewma
from .water import nh3_fraction, do_saturation, tan_capacity_q10
from .dynamics import cstr_concentration
from .growth import tgc_growth
from .alerts import Alert, check_threshold

__all__ = [
    "hampel_filter",
    "ewma",
    "nh3_fraction",
    "do_saturation",
    "tan_capacity_q10",
    "cstr_concentration",
    "tgc_growth",
    "Alert",
    "check_threshold",

"""Utilities for aquaponics calculations."""

from .kpis import feed_conversion_ratio

__all__ = ["feed_conversion_ratio"]

