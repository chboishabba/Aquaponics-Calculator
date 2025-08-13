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
