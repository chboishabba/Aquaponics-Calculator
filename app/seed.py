from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import (
    Species,
    WaterTarget,
    SourceTag,
    HumanFood,
    FeedIngredient,
    SeasonalYield,
    ProcessingLossFactor,
)
from .etl import load_ausnut, load_fdc, load_feedipedia, load_aquaculture

def seed():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Species)).first():
            defaults = [
                {"common_name": "tilapia"},
                {"common_name": "trout"},
                {"common_name": "basil"},
                {"common_name": "lettuce"},
            ]
            for data in defaults:
                session.add(Species(**data))
        if not session.exec(select(WaterTarget)).first():
            targets = [
                {"parameter": "pH", "min_value": 6.5, "max_value": 7.5},
                {"parameter": "temp", "min_value": 20, "max_value": 28},
                {"parameter": "DO", "min_value": 5, "max_value": 8},
            ]
            for t in targets:
                session.add(WaterTarget(**t))

        if not session.exec(select(SourceTag)).first():
            tags = [
                {"name": "AUSNUT"},
                {"name": "USDA FDC"},
                {"name": "Feedipedia"},
                {"name": "Aquaculture Table"},
            ]
            for t in tags:
                session.add(SourceTag(**t))

        session.commit()

        # Run ETL loaders (they silently skip if data files are missing)
        load_ausnut(session)
        load_fdc(session)
        load_feedipedia(session)
        load_aquaculture(session)

        if not session.exec(select(HumanFood)).first():
            ausnut_tag = session.exec(
                select(SourceTag).where(SourceTag.name == "AUSNUT")
            ).first()
            session.add(HumanFood(name="Tomato", source_tag_id=ausnut_tag.tag_id, available_on_farm=True))
            session.add(HumanFood(name="Rice", source_tag_id=ausnut_tag.tag_id, available_on_farm=False))

        if not session.exec(select(FeedIngredient)).first():
            feed_tag = session.exec(
                select(SourceTag).where(SourceTag.name == "Feedipedia")
            ).first()
            session.add(FeedIngredient(name="Soy Meal", source_tag_id=feed_tag.tag_id, available_on_farm=False))
            session.add(FeedIngredient(name="Duckweed", source_tag_id=feed_tag.tag_id, available_on_farm=True))

        if not session.exec(select(SeasonalYield)).first():
            tomato = session.exec(select(HumanFood).where(HumanFood.name == "Tomato")).first()
            if tomato:
                session.add(SeasonalYield(food_id=tomato.food_id, season="Summer", yield_kg=1.2))

        if not session.exec(select(ProcessingLossFactor)).first():
            tomato = session.exec(select(HumanFood).where(HumanFood.name == "Tomato")).first()
            if tomato:
                session.add(ProcessingLossFactor(food_id=tomato.food_id, process="Cleaning", loss_factor=0.1))

        session.commit()

if __name__ == "__main__":
    seed()
