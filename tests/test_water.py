import math
import pytest
from aquaponics.water import nh3_fraction, do_saturation, tan_capacity_q10

def test_nh3_fraction_known_value():
    frac = nh3_fraction(pH=8.0, temp_c=25.0)
    assert abs(frac - 0.053) < 0.005

def test_do_saturation_20c():
    sat = do_saturation(20.0)
    assert abs(sat - 9.08) < 0.1

def test_tan_capacity_q10():
    cap = tan_capacity_q10(surface_area_m2=10, base_rate=1, temp_c=30)
    assert math.isclose(cap, 10 * 1.5)


def test_water_negative_inputs():
    with pytest.raises(ValueError):
        nh3_fraction(pH=7.0, temp_c=-1)
    with pytest.raises(ValueError):
        do_saturation(-1)
    with pytest.raises(ValueError):
        tan_capacity_q10(surface_area_m2=-1, base_rate=1, temp_c=20)
    with pytest.raises(ValueError):
        tan_capacity_q10(surface_area_m2=1, base_rate=-1, temp_c=20)
    with pytest.raises(ValueError):
        tan_capacity_q10(surface_area_m2=1, base_rate=1, temp_c=-20)
    with pytest.raises(ValueError):
        tan_capacity_q10(surface_area_m2=1, base_rate=1, temp_c=20, ref_temp_c=-5)
