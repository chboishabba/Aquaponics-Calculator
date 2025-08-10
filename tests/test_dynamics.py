from aquaponics.dynamics import cstr_concentration
import math

def test_cstr_concentration():
    c = cstr_concentration(initial_conc=10, inflow_conc=0, flow_rate=100, volume=1000, time=1)
    assert math.isclose(c, 10 * math.exp(-0.1), rel_tol=1e-5)
