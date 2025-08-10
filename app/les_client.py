"""Client for interfacing with the LES simulation service."""
from __future__ import annotations

from datetime import datetime
import json
import os
from typing import Dict, Any

import httpx


class LESClient:
    """Simple HTTP client for the LES environmental simulator.

    The client sends diet or feed plans to the LES service and
    returns key environmental KPIs such as oxygen demand and
    nutrient cycling efficiency.
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def run_simulation(self, plan: Dict[str, float]) -> Dict[str, Any]:
        """Submit a plan to LES and return parsed KPIs."""
        try:
            resp = httpx.post(f"{self.base_url}/simulate", json={"plan": plan})
            resp.raise_for_status()
        except httpx.HTTPError as exc:  # pragma: no cover - network failure
            raise RuntimeError(f"LES request failed: {exc}") from exc
        data = resp.json()
        return {
            "oxygen_demand": data.get("oxygen_demand"),
            "nutrient_cycling": data.get("nutrient_cycling"),
            **{k: v for k, v in data.items() if k not in {"oxygen_demand", "nutrient_cycling"}},
        }

    def save_report(self, plan: Dict[str, float], kpis: Dict[str, Any], directory: str = "data/reports") -> str:
        """Store a scenario report for later comparison."""
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        path = os.path.join(directory, f"scenario_{timestamp}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"plan": plan, "kpis": kpis, "timestamp": timestamp}, f, indent=2)
        return path
