import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from aquaponics import condition_factor, survival_rate


def test_survival_rate_standard_case() -> None:
    assert survival_rate(100, 80) == pytest.approx(80.0)


def test_survival_rate_initial_zero() -> None:
    with pytest.raises(ValueError):
        survival_rate(0, 10)


def test_survival_rate_final_negative() -> None:
    with pytest.raises(ValueError):
        survival_rate(100, -5)


def test_condition_factor_standard_case() -> None:
    # Example: weight 500g, length 25cm -> K = 3.2
    assert condition_factor(500, 25) == pytest.approx(3.2)


def test_condition_factor_length_zero() -> None:
    with pytest.raises(ValueError):
        condition_factor(100, 0)


def test_condition_factor_weight_negative() -> None:
    with pytest.raises(ValueError):
        condition_factor(-1, 10)

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
