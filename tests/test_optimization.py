from app.optimization import optimize_feed, optimize_menu


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
