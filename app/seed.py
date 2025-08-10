from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import Species, WaterTarget

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
        session.commit()

if __name__ == "__main__":
    seed()
