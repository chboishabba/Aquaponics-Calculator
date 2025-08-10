from typing import Dict, List, Optional

try:
    from ortools.linear_solver import pywraplp
except Exception:  # pragma: no cover - fallback when ortools missing
    pywraplp = None


def optimize_menu(ingredients: List[Dict], requirements: Dict[str, float], les_client: Optional[object] = None):
    """Simple linear program for a human menu.

    Args:
        ingredients: list of dicts with keys name, cost, nutrients (dict).
        requirements: nutrient -> minimum requirement.
    Returns:
        dict mapping ingredient names to grams per day.
    """
    if pywraplp:
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("GLOP solver unavailable")

        variables = {
            ing["name"]: solver.NumVar(0, solver.infinity(), ing["name"]) for ing in ingredients
        }
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
            raise ValueError("No optimal menu found")

        solution = {name: var.solution_value() for name, var in variables.items()}
    else:
        # Fallback: pick cheapest ingredient satisfying each nutrient independently
        solution: Dict[str, float] = {ing["name"]: 0 for ing in ingredients}
        for nutrient, minimum in requirements.items():
            best = min(
                ingredients,
                key=lambda ing: (
                    float("inf")
                    if ing["nutrients"].get(nutrient, 0) == 0
                    else ing.get("cost", 0) / ing["nutrients"].get(nutrient, 0)
                ),
            )
            needed = minimum / best["nutrients"].get(nutrient, 1)
            solution[best["name"]] = max(solution[best["name"]], needed)
    if les_client:
        kpis = les_client.run_simulation(solution)
        return {"plan": solution, "kpis": kpis}
    return solution


def optimize_feed(ingredients: List[Dict], requirements: Dict[str, float], les_client: Optional[object] = None):
    """Least cost fish feed formulation."""
    if pywraplp:
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if solver is None:
            raise RuntimeError("GLOP solver unavailable")

        variables = {
            ing["name"]: solver.NumVar(0, 1, ing["name"]) for ing in ingredients
        }
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

        solution = {name: var.solution_value() for name, var in variables.items()}
    else:
        # Fallback heuristic: allocate nutrient using cheapest ingredient
        solution: Dict[str, float] = {ing["name"]: 0 for ing in ingredients}
        for nutrient, minimum in requirements.items():
            best = min(
                ingredients,
                key=lambda ing: (
                    float("inf")
                    if ing["nutrients"].get(nutrient, 0) == 0
                    else ing.get("cost", 0) / ing["nutrients"].get(nutrient, 0)
                ),
            )
            needed = minimum / best["nutrients"].get(nutrient, 1)
            solution[best["name"]] = max(solution[best["name"]], needed)
        total = sum(solution.values()) or 1.0
        solution = {name: value / total for name, value in solution.items()}
    if les_client:
        kpis = les_client.run_simulation(solution)
        return {"plan": solution, "kpis": kpis}
    return solution
