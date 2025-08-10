from typing import Dict, List, Tuple
from sqlmodel import SQLModel, create_engine, Session, select

from .models import (
    FeedIngredient,
    FeedRequirement,
    Ingredient,
    PersonaRequirement,
)

DATABASE_URL = "sqlite:///aquaponics.db"

def get_engine():
    return create_engine(DATABASE_URL, echo=False)

engine = get_engine()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


def get_menu_inputs(
    session: Session, persona: str
) -> Tuple[List[Dict], Dict[str, float], Dict[str, float], Dict[str, float], Dict[str, float]]:
    """Fetch ingredients, requirements and constraints for a persona."""

    ingredients: List[Dict] = []
    preferences: Dict[str, float] = {}
    caps: Dict[str, float] = {}
    inventory: Dict[str, float] = {}
    for ing in session.exec(select(Ingredient)).all():
        ingredients.append(
            {"name": ing.name, "cost": ing.cost_per_kg, "nutrients": ing.nutrients}
        )
        inventory[ing.name] = ing.stock_on_hand
        if ing.cap is not None:
            caps[ing.name] = ing.cap
        if persona in ing.preferences:
            preferences[ing.name] = ing.preferences[persona]

    requirements: Dict[str, float] = {}
    query = select(PersonaRequirement).where(PersonaRequirement.persona == persona)
    for req in session.exec(query).all():
        requirements[req.nutrient] = req.amount

    return ingredients, requirements, preferences, caps, inventory


def get_feed_inputs(
    session: Session,
) -> Tuple[List[Dict], Dict[str, float], Dict[str, float], Dict[str, float]]:
    """Fetch feed formulation inputs from the database."""

    ingredients: List[Dict] = []
    caps: Dict[str, float] = {}
    inventory: Dict[str, float] = {}
    for ing in session.exec(select(FeedIngredient)).all():
        ingredients.append(
            {"name": ing.name, "cost": ing.cost_per_kg, "nutrients": ing.nutrients}
        )
        inventory[ing.name] = ing.stock_on_hand
        if ing.cap is not None:
            caps[ing.name] = ing.cap

    requirements: Dict[str, float] = {}
    for req in session.exec(select(FeedRequirement)).all():
        requirements[req.nutrient] = req.amount

    return ingredients, requirements, caps, inventory
