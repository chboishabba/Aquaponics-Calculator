from typing import Dict, List, Optional

try:
    from ortools.linear_solver import pywraplp
except Exception:  # pragma: no cover - fallback when ortools missing
    pywraplp = None


def optimize_menu(
    ingredients: List[Dict],
    requirements: Dict[str, float],
    preferences: Optional[Dict[str, float]] = None,
    caps: Optional[Dict[str, float]] = None,
    inventory: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """Simple linear program for a human menu with optional constraints.

    Args:
        ingredients: list of dicts with keys name, cost, nutrients (dict).
        requirements: nutrient -> minimum requirement.
        preferences: ingredient -> bonus/penalty applied to objective (positive favors).
        caps: ingredient -> maximum inclusion amount.
        inventory: ingredient -> available inventory shared across personas.
    Returns:
        dict mapping ingredient names to grams per day.
    """
    preferences = preferences or {}
    caps = caps or {}
    inventory = inventory or {}

    if pywraplp:
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("GLOP solver unavailable")

        variables = {}
        for ing in ingredients:
            name = ing["name"]
            upper = solver.infinity()
            if name in caps:
                upper = min(upper, caps[name])
            if name in inventory:
                upper = min(upper, inventory[name])
            variables[name] = solver.NumVar(0, upper, name)

        solver.Minimize(
            solver.Sum(
                variables[ing["name"]]
                * (ing.get("cost", 0) - preferences.get(ing["name"], 0))
                for ing in ingredients
            )
        )

        for nutrient, minimum in requirements.items():
            solver.Add(
                solver.Sum(
                    variables[ing["name"]] * ing["nutrients"].get(nutrient, 0)
                    for ing in ingredients
                )
                >= minimum
            )

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:
            raise ValueError("No optimal menu found")

        return {name: var.solution_value() for name, var in variables.items()}
    # Fallback: pick cheapest ingredient satisfying each nutrient independently
    solution: Dict[str, float] = {ing["name"]: 0 for ing in ingredients}
    for nutrient, minimum in requirements.items():
        remaining = minimum
        # sort ingredients by adjusted cost per unit nutrient
        sorted_ings = sorted(
            ingredients,
            key=lambda ing: (
                float("inf")
                if ing["nutrients"].get(nutrient, 0) == 0
                else (ing.get("cost", 0) - preferences.get(ing["name"], 0))
                / ing["nutrients"].get(nutrient, 0)
            ),
        )
        for ing in sorted_ings:
            contrib = ing["nutrients"].get(nutrient, 0)
            if contrib <= 0:
                continue
            name = ing["name"]
            allowed = min(
                caps.get(name, float("inf")),
                inventory.get(name, float("inf")),
            )
            available = max(0, allowed - solution[name])
            if available <= 0:
                continue
            take = min(remaining / contrib, available)
            solution[name] += take
            remaining -= take * contrib
            if remaining <= 0:
                break
    return solution


def optimize_feed(
    ingredients: List[Dict],
    requirements: Dict[str, float],
    caps: Optional[Dict[str, float]] = None,
    inventory: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """Least cost fish feed formulation with optional caps and inventory limits."""
    caps = caps or {}
    inventory = inventory or {}
    if pywraplp:
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("GLOP solver unavailable")

        variables = {}
        for ing in ingredients:
            name = ing["name"]
            upper = 1.0
            if name in caps:
                upper = min(upper, caps[name])
            if name in inventory:
                upper = min(upper, inventory[name])
            variables[name] = solver.NumVar(0, upper, name)
        solver.Add(solver.Sum(variables.values()) == 1)
        solver.Minimize(
            solver.Sum(variables[ing["name"]] * ing.get("cost", 0) for ing in ingredients)
        )

        for nutrient, minimum in requirements.items():
            solver.Add(
                solver.Sum(
                    variables[ing["name"]] * ing["nutrients"].get(nutrient, 0)
                    for ing in ingredients
                )
                >= minimum
            )

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:
            raise ValueError("No optimal feed found")

        return {name: var.solution_value() for name, var in variables.items()}
    # Fallback heuristic: allocate nutrient using cheapest ingredient
    solution: Dict[str, float] = {ing["name"]: 0 for ing in ingredients}
    for nutrient, minimum in requirements.items():
        remaining = minimum
        sorted_ings = sorted(
            ingredients,
            key=lambda ing: (
                float("inf")
                if ing["nutrients"].get(nutrient, 0) == 0
                else ing.get("cost", 0) / ing["nutrients"].get(nutrient, 0)
            ),
        )
        for ing in sorted_ings:
            contrib = ing["nutrients"].get(nutrient, 0)
            if contrib <= 0:
                continue
            name = ing["name"]
            allowed = min(
                caps.get(name, float("inf")),
                inventory.get(name, float("inf")),
            )
            available = max(0, allowed - solution[name])
            if available <= 0:
                continue
            take = min(remaining / contrib, available)
            solution[name] += take
            remaining -= take * contrib
            if remaining <= 0:
                break
    total = sum(solution.values()) or 1.0
    return {name: value / total for name, value in solution.items()}
