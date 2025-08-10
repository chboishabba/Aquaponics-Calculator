"""ETL for USDA FoodData Central."""

import csv
from pathlib import Path
from sqlmodel import Session, select
from ..models import HumanFood, SourceTag

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "fdc.csv"


def load(session: Session, data_file: Path = DATA_FILE) -> None:
    """Load USDA FDC CSV data into the HumanFood table."""
    if not data_file.exists():
        return

    tag = session.exec(select(SourceTag).where(SourceTag.name == "USDA FDC")).first()
    if not tag:
        tag = SourceTag(name="USDA FDC")
        session.add(tag)
        session.commit()
        session.refresh(tag)

    with data_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            food = HumanFood(
                name=row["name"],
                source_tag_id=tag.tag_id,
                available_on_farm=row.get("available_on_farm", "").lower() == "true",
            )
            session.add(food)
    session.commit()
