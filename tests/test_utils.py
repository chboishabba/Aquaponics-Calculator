import os
import sys
import types

import pytest

# Ensure the application package is importable when tests are run directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub out modules with syntax errors so app.utils can be imported.
database_stub = types.ModuleType("app.database")
database_stub.get_menu_inputs = lambda *args, **kwargs: ([], {})
database_stub.get_feed_inputs = lambda *args, **kwargs: ([], {})
optimization_stub = types.ModuleType("app.optimization")
optimization_stub.optimize_menu = lambda *args, **kwargs: {}
optimization_stub.optimize_feed = lambda *args, **kwargs: {}

sys.modules.setdefault("app.database", database_stub)
sys.modules.setdefault("app.optimization", optimization_stub)

from app.utils import run_optimizations, tan_load_check


def test_tan_load_check_normal_case():
    utilization, ok = tan_load_check(100, 10)
    assert utilization == pytest.approx(92.0)
    assert ok is True


@pytest.mark.parametrize("biofilter_cap_g", [0, -1])
def test_tan_load_check_invalid_capacity(biofilter_cap_g):
    with pytest.raises(ValueError):
        tan_load_check(100, biofilter_cap_g)


def test_run_optimizations_aggregates_results(monkeypatch):
    def fake_get_menu_inputs(session, persona):
        assert session == "dummy_session"
        assert persona == "p1"
        return (1, 2)

    def fake_optimize_menu(a, b):
        assert (a, b) == (1, 2)
        return {"menu_result": 42}

    def fake_get_feed_inputs(session):
        assert session == "dummy_session"
        return (3, 4)

    def fake_optimize_feed(a, b):
        assert (a, b) == (3, 4)
        return {"feed_result": 24}

    monkeypatch.setattr("app.utils.get_menu_inputs", fake_get_menu_inputs)
    monkeypatch.setattr("app.utils.optimize_menu", fake_optimize_menu)
    monkeypatch.setattr("app.utils.get_feed_inputs", fake_get_feed_inputs)
    monkeypatch.setattr("app.utils.optimize_feed", fake_optimize_feed)

    result = run_optimizations("dummy_session", "p1")
    assert result == {"menu": {"menu_result": 42}, "feed": {"feed_result": 24}}
