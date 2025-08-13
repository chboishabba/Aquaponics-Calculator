import math
import pytest
from aquaponics.water import nh3_fraction, do_saturation, tan_capacity_q10

def test_nh3_fraction_known_value():
    frac = nh3_fraction(pH=8.0, temp_c=25.0)
    assert abs(frac - 0.053) < 0.005


def test_nh3_fraction_invalid_ph():
    with pytest.raises(ValueError, match="pH must be between 0 and 14"):
        nh3_fraction(pH=-1, temp_c=25.0)

def test_do_saturation_20c():
    sat = do_saturation(20.0)
    assert abs(sat - 9.08) < 0.1


def test_do_saturation_invalid_temp():
    with pytest.raises(ValueError, match="temp_c must be between 0 and 40"):
        do_saturation(-5.0)

def test_tan_capacity_q10():
    cap = tan_capacity_q10(surface_area_m2=10, base_rate=1, temp_c=30)
    assert math.isclose(cap, 10 * 1.5)


def test_tan_capacity_q10_invalid_surface_area():
    with pytest.raises(ValueError, match="surface_area_m2 must be non-negative"):
        tan_capacity_q10(surface_area_m2=-1, base_rate=1, temp_c=20)
