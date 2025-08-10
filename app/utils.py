def tan_load_check(protein_feed_g: float, biofilter_cap_g: float):
    """Evaluate if the biofilter can handle TAN generated from protein feed.

    Approximately 9.2% of feed protein is converted to total ammonia nitrogen (TAN).
    This function estimates TAN load and compares it to the biofilter capacity.

    Args:
        protein_feed_g: Amount of protein feed provided (g).
        biofilter_cap_g: Biofilter capacity for TAN (g).

    Returns:
        A tuple ``(utilization_pct, within_capacity)`` where ``utilization_pct`` is
        the percentage of the biofilter capacity used and ``within_capacity``
        indicates whether the TAN load is within the biofilter's handling ability.
    """
    if biofilter_cap_g <= 0:
        raise ValueError("biofilter_cap_g must be positive")

    tan_produced = protein_feed_g * 0.092
    utilization_pct = (tan_produced / biofilter_cap_g) * 100
    return utilization_pct, utilization_pct <= 100


from typing import Dict
from sqlmodel import Session

from .database import get_feed_inputs, get_menu_inputs
from .optimization import optimize_feed, optimize_menu


def run_optimizations(session: Session, persona: str) -> Dict[str, Dict[str, float]]:
    """Run both menu and feed optimizations and aggregate the results."""

    menu_inputs = get_menu_inputs(session, persona)
    menu_solution = optimize_menu(*menu_inputs)

    feed_inputs = get_feed_inputs(session)
    feed_solution = optimize_feed(*feed_inputs)

    return {"menu": menu_solution, "feed": feed_solution}


def _cli(persona: str) -> None:
    """Simple CLI for running both optimizers."""
    from .database import get_engine

    engine = get_engine()
    with Session(engine) as session:
        result = run_optimizations(session, persona)
    print(result)


if __name__ == "__main__":  # pragma: no cover - manual utility
    import argparse

    parser = argparse.ArgumentParser(description="Run optimizations")
    parser.add_argument("persona", help="Persona name for menu optimization")
    args = parser.parse_args()
    _cli(args.persona)
