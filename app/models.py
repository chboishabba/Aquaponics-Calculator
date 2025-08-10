from datetime import datetime, date
from typing import Dict, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class Species(SQLModel, table=True):
    __tablename__ = "species"
    species_id: Optional[int] = Field(default=None, primary_key=True)
    common_name: str
    latin_name: Optional[str] = None

class StockBatch(SQLModel, table=True):
    __tablename__ = "stock_batches"
    batch_id: Optional[int] = Field(default=None, primary_key=True)
    species_id: int = Field(foreign_key="species.species_id")
    start_date: Optional[date] = None

class WaterTarget(SQLModel, table=True):
    __tablename__ = "water_targets"
    target_id: Optional[int] = Field(default=None, primary_key=True)
    parameter: str
    min_value: float
    max_value: float
    location: Optional[str] = None

class WaterReading(SQLModel, table=True):
    __tablename__ = "water_readings"
    reading_id: Optional[int] = Field(default=None, primary_key=True)
    parameter: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None

class FeedLog(SQLModel, table=True):
    __tablename__ = "feed_logs"
    feed_log_id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="stock_batches.batch_id")
    amount_g: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GrowthRecord(SQLModel, table=True):
    __tablename__ = "growth_records"
    record_id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="stock_batches.batch_id")
    weight_avg_g: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class EventLog(SQLModel, table=True):
    __tablename__ = "event_logs"
    event_id: Optional[int] = Field(default=None, primary_key=True)
    reading_id: int = Field(foreign_key="water_readings.reading_id")
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str = "kg"
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    source: Optional[str] = None
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    preferences: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class FeedIngredient(SQLModel, table=True):
    __tablename__ = "feed_ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str = "kg"
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    source: Optional[str] = None
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class Nutrient(SQLModel, table=True):
    __tablename__ = "nutrients"
    nutrient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str


class PersonaRequirement(SQLModel, table=True):
    """Nutrient requirements for a given persona."""

    __tablename__ = "persona_requirements"
    id: Optional[int] = Field(default=None, primary_key=True)
    persona: str
    nutrient: str
    amount: float


class FeedRequirement(SQLModel, table=True):
    """Global nutrient requirements for formulating feed."""

    __tablename__ = "feed_requirements"
    id: Optional[int] = Field(default=None, primary_key=True)
    nutrient: str
    amount: float
