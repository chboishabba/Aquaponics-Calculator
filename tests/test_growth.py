import pytest
from aquaponics.growth import tgc_growth

def test_tgc_growth():
    final_w = tgc_growth(initial_weight_g=100, tgc=0.2, temp_sum=200)
    assert round(final_w, 2) == round((100 ** (1/3) + 0.2*200/1000) ** 3, 2)


def test_tgc_growth_negative_values():
    with pytest.raises(ValueError):
        tgc_growth(initial_weight_g=-1, tgc=0.2, temp_sum=200)
    with pytest.raises(ValueError):
        tgc_growth(initial_weight_g=100, tgc=-0.2, temp_sum=200)
    with pytest.raises(ValueError):
        tgc_growth(initial_weight_g=100, tgc=0.2, temp_sum=-200)
def test_tgc_growth_invalid_initial_weight():
    with pytest.raises(ValueError, match="initial_weight_g must be positive"):
        tgc_growth(initial_weight_g=-1, tgc=0.2, temp_sum=100)


def test_tgc_growth_invalid_tgc():
    with pytest.raises(ValueError, match="tgc must be positive"):
        tgc_growth(initial_weight_g=100, tgc=0, temp_sum=100)


def test_tgc_growth_invalid_temp_sum():
    with pytest.raises(ValueError, match="temp_sum must be non-negative"):
        tgc_growth(initial_weight_g=100, tgc=0.2, temp_sum=-1)
