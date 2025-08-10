import pytest

from aquaponics import feed_conversion_ratio


def test_feed_conversion_ratio_normal_case():
    assert feed_conversion_ratio(2.0, 1.0) == 2.0


def test_feed_conversion_ratio_zero_feed():
    assert feed_conversion_ratio(0.0, 1.0) == 0.0


@pytest.mark.parametrize(
    "feed_mass_kg, biomass_gain_kg",
    [(-1.0, 1.0), (1.0, 0.0), (1.0, -0.5)],
)
def test_feed_conversion_ratio_invalid_inputs(feed_mass_kg, biomass_gain_kg):
    with pytest.raises(ValueError):
        feed_conversion_ratio(feed_mass_kg, biomass_gain_kg)
