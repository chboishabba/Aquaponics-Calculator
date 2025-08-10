"""Aquaponics key performance indicators."""

from __future__ import annotations


def survival_rate(initial_count: float, final_count: float) -> float:
    """Calculate the survival rate percentage.

    Parameters
    ----------
    initial_count: float
        The initial number of organisms at the start of the period.
    final_count: float
        The number of organisms remaining at the end of the period.

    Returns
    -------
    float
        The survival rate expressed as a percentage.

    Raises
    ------
    ValueError
        If ``initial_count`` is less than or equal to zero or ``final_count`` is
        negative.
    """
    if initial_count <= 0:
        raise ValueError("initial_count must be positive")
    if final_count < 0:
        raise ValueError("final_count must be non-negative")
    return final_count / initial_count * 100


def condition_factor(weight_g: float, length_cm: float) -> float:
    """Compute the Fulton condition factor (K).

    Parameters
    ----------
    weight_g: float
        Weight of the organism in grams.
    length_cm: float
        Length of the organism in centimeters.

    Returns
    -------
    float
        The condition factor ``K = 100 * weight / length^3``.

    Raises
    ------
    ValueError
        If ``weight_g`` is negative or ``length_cm`` is less than or equal to
        zero.
    """
    if weight_g < 0:
        raise ValueError("weight_g must be non-negative")
    if length_cm <= 0:
        raise ValueError("length_cm must be positive")
    return 100 * weight_g / (length_cm ** 3)
