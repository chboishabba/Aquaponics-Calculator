"""ETL for aquaculture feed tables."""

import csv
from pathlib import Path
from sqlmodel import Session, select
from ..models import FeedIngredient, SourceTag

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "aquaculture.csv"


def load(session: Session, data_file: Path = DATA_FILE) -> None:
    """Load aquaculture CSV data into the FeedIngredient table."""
    if not data_file.exists():
        return

    tag = session.exec(select(SourceTag).where(SourceTag.name == "Aquaculture Table")).first()
    if not tag:
        tag = SourceTag(name="Aquaculture Table")
        session.add(tag)
        session.commit()
        session.refresh(tag)

    with data_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            ingredient = FeedIngredient(
                name=row["name"],
                source_tag_id=tag.tag_id,
                available_on_farm=row.get("available_on_farm", "").lower() == "true",
            )
            session.add(ingredient)
    session.commit()
