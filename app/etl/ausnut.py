"""ETL for AUSNUT food composition data."""

import csv
from pathlib import Path
from sqlmodel import Session, select
from ..models import HumanFood, SourceTag

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "ausnut.csv"


def load(session: Session, data_file: Path = DATA_FILE) -> None:
    """Load AUSNUT CSV data into the HumanFood table.

    The CSV is expected to contain at least a ``name`` column and an optional
    ``available_on_farm`` boolean column.
    """
    if not data_file.exists():
        return

    tag = session.exec(select(SourceTag).where(SourceTag.name == "AUSNUT")).first()
    if not tag:
        tag = SourceTag(name="AUSNUT")
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
