from app.optimization import optimize_feed, optimize_menu
from sqlmodel import SQLModel, Session, create_engine

from app.models import (
    FeedIngredient,
    FeedRequirement,
    Ingredient,
    PersonaRequirement,
)
from app.utils import run_optimizations


def test_optimize_feed():
    ingredients = [
        {"name": "duckweed", "cost": 1.0, "nutrients": {"protein": 0.4, "energy": 2}},
        {"name": "soy", "cost": 0.8, "nutrients": {"protein": 0.5, "energy": 2.5}},
    ]
    requirements = {"protein": 0.5}
    result = optimize_feed(ingredients, requirements)
    assert abs(sum(result.values()) - 1.0) < 1e-6
    protein = sum(result[i["name"]] * i["nutrients"]["protein"] for i in ingredients)
    assert protein >= requirements["protein"] - 1e-6


def test_optimize_menu():
    ingredients = [
        {"name": "lettuce", "cost": 2.0, "nutrients": {"energy": 0.1, "protein": 0.02}},
        {"name": "tilapia", "cost": 5.0, "nutrients": {"energy": 1.0, "protein": 0.2}},
    ]
    requirements = {"protein": 0.1}
    result = optimize_menu(ingredients, requirements)
    protein = sum(result[i["name"]] * i["nutrients"]["protein"] for i in ingredients)
    assert protein >= requirements["protein"] - 1e-6


def test_optimize_menu_caps_inventory():
    ingredients = [
        {"name": "a", "cost": 1.0, "nutrients": {"protein": 1}},
        {"name": "b", "cost": 1.0, "nutrients": {"protein": 1}},
    ]
    requirements = {"protein": 6}
    caps = {"a": 4}
    inventory = {"a": 5, "b": 2}
    result = optimize_menu(ingredients, requirements, caps=caps, inventory=inventory)
    assert result["a"] <= 4 + 1e-6
    assert result["b"] <= 2 + 1e-6
    protein = sum(result[i["name"]] * i["nutrients"]["protein"] for i in ingredients)
    assert protein >= requirements["protein"] - 1e-6


def test_run_optimizations_with_db():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(
            Ingredient(
                name="a",
                cost_per_kg=1,
                stock_on_hand=5,
                nutrients={"protein": 1},
                cap=4,
            )
        )
        session.add(
            Ingredient(
                name="b",
                cost_per_kg=1,
                stock_on_hand=2,
                nutrients={"protein": 1},
            )
        )
        session.add(
            PersonaRequirement(persona="p1", nutrient="protein", amount=6)
        )
        session.add(
            FeedIngredient(
                name="f1",
                cost_per_kg=1,
                stock_on_hand=1,
                nutrients={"protein": 1},
                cap=0.5,
            )
        )
        session.add(
            FeedIngredient(
                name="f2",
                cost_per_kg=2,
                stock_on_hand=1,
                nutrients={"protein": 1},
            )
        )
        session.add(FeedRequirement(nutrient="protein", amount=1))
        session.commit()
        result = run_optimizations(session, "p1")

    menu = result["menu"]
    assert menu["a"] <= 4 + 1e-6
    assert menu["b"] <= 2 + 1e-6
    protein = menu["a"] + menu["b"]
    assert protein >= 6 - 1e-6

    feed = result["feed"]
    assert feed["f1"] <= 0.5 + 1e-6
    assert abs(sum(feed.values()) - 1.0) < 1e-6
