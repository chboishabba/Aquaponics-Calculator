import sys
from pathlib import Path

import pytest

# Ensure project root is on the import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from aquaponics.alerts import calculate_warn_range


def test_warn_pct_out_of_bounds():
    with pytest.raises(ValueError, match="0 <= warn_pct < 0.5"):
        calculate_warn_range(0, 10, -0.1)
    with pytest.raises(ValueError, match="0 <= warn_pct < 0.5"):
        calculate_warn_range(0, 10, 0.5)


def test_max_value_gt_min_value():
    with pytest.raises(ValueError, match="max_value must be greater than min_value"):
        calculate_warn_range(5, 5, 0.1)
    with pytest.raises(ValueError, match="max_value must be greater than min_value"):
        calculate_warn_range(10, 5, 0.1)
