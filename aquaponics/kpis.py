"""Key performance indicators for aquaponics systems."""

from __future__ import annotations


def feed_conversion_ratio(feed_mass_kg: float, biomass_gain_kg: float) -> float:
    """Calculate the feed conversion ratio (FCR).

    The FCR is the amount of feed provided divided by the resulting gain in
    biomass. ``feed_mass_kg`` must be non-negative and ``biomass_gain_kg`` must
    be greater than zero.

    Args:
        feed_mass_kg: Mass of feed provided in kilograms.
        biomass_gain_kg: Increase in biomass in kilograms.

    Returns:
        The feed conversion ratio as a float.

    Raises:
        ValueError: If ``feed_mass_kg`` is negative or ``biomass_gain_kg`` is not
        positive.
    """
    if feed_mass_kg < 0:
        raise ValueError("feed_mass_kg must be non-negative")
    if biomass_gain_kg <= 0:
        raise ValueError("biomass_gain_kg must be greater than zero")
    return feed_mass_kg / biomass_gain_kg
