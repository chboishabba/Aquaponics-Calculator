import sys
import types
from typing import Dict, Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, Session, SQLModel, create_engine


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    preferences: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class PersonaRequirement(SQLModel, table=True):
    __tablename__ = "persona_requirements"
    id: Optional[int] = Field(default=None, primary_key=True)
    persona: str
    nutrient: str
    amount: float


class FeedIngredient(SQLModel, table=True):
    __tablename__ = "feed_ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class FeedRequirement(SQLModel, table=True):
    __tablename__ = "feed_requirements"
    id: Optional[int] = Field(default=None, primary_key=True)
    nutrient: str
    amount: float


# Inject a fake `app.models` module so database functions can import it
fake_models = types.ModuleType("app.models")
fake_models.Ingredient = Ingredient
fake_models.PersonaRequirement = PersonaRequirement
fake_models.FeedIngredient = FeedIngredient
fake_models.FeedRequirement = FeedRequirement
sys.modules.setdefault("app.models", fake_models)

from app.database import get_menu_inputs, get_feed_inputs


def _setup_engine():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    return engine


def test_get_menu_inputs():
    engine = _setup_engine()
    with Session(engine) as session:
        session.add(
            Ingredient(
                name="carrot",
                cost_per_kg=1.5,
                stock_on_hand=2,
                nutrients={"vitamin": 10},
                preferences={"p1": 0.8},
                cap=3,
            )
        )
        session.add(
            PersonaRequirement(persona="p1", nutrient="vitamin", amount=5)
        )
        session.commit()
        ingredients, requirements, preferences, caps, inventory = get_menu_inputs(
            session, "p1"
        )

    assert ingredients == [
        {"name": "carrot", "cost": 1.5, "nutrients": {"vitamin": 10}}
    ]
    assert requirements == {"vitamin": 5}
    assert preferences == {"carrot": 0.8}
    assert caps == {"carrot": 3}
    assert inventory == {"carrot": 2}


def test_get_feed_inputs():
    engine = _setup_engine()
    with Session(engine) as session:
        session.add(
            FeedIngredient(
                name="corn",
                cost_per_kg=0.5,
                stock_on_hand=10,
                nutrients={"protein": 0.2},
                cap=5,
            )
        )
        session.add(FeedRequirement(nutrient="protein", amount=0.1))
        session.commit()
        ingredients, requirements, caps, inventory = get_feed_inputs(session)

    assert ingredients == [
        {"name": "corn", "cost": 0.5, "nutrients": {"protein": 0.2}}
    ]
    assert requirements == {"protein": 0.1}
    assert caps == {"corn": 5}
    assert inventory == {"corn": 10}
