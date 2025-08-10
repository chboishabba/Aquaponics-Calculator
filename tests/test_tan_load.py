import os
import sys

import pytest

# Ensure the application package is importable when tests are run directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils import tan_load_check

def test_tan_load_within_capacity():
    utilization, ok = tan_load_check(100, 10)
    assert utilization == pytest.approx(92.0)
    assert ok is True

def test_tan_load_exceeds_capacity():
    utilization, ok = tan_load_check(200, 10)
    assert utilization == pytest.approx(184.0)
    assert ok is False

def test_zero_feed():
    utilization, ok = tan_load_check(0, 10)
    assert utilization == 0
    assert ok is True

def test_zero_capacity_raises():
    with pytest.raises(ValueError):
        tan_load_check(100, 0)
