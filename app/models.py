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
    expected_harvest_date: Optional[date] = None
    expected_yield_kg: Optional[float] = None
    yield_std_kg: Optional[float] = None

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

class SourceTag(SQLModel, table=True):
    __tablename__ = "source_tags"
    tag_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    on_farm: bool = False
    description: Optional[str] = None


class HumanFood(SQLModel, table=True):
    __tablename__ = "human_foods"
    food_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source_tag_id: Optional[int] = Field(default=None, foreign_key="source_tags.tag_id")
    available_on_farm: bool = False
=======
    unit: str = "kg"
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    source: Optional[str] = None
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    preferences: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class InventorySnapshot(SQLModel, table=True):
    __tablename__ = "inventory_snapshots"
    snapshot_id: Optional[int] = Field(default=None, primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.ingredient_id")
    stock_on_hand: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedIngredient(SQLModel, table=True):
    __tablename__ = "feed_ingredients"
    ingredient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str = "kg"
    cost_per_kg: float = 0
    stock_on_hand: float = 0
    source_tag_id: Optional[int] = Field(default=None, foreign_key="source_tags.tag_id")
    available_on_farm: bool = False


class SeasonalYield(SQLModel, table=True):
    __tablename__ = "seasonal_yields"
    yield_id: Optional[int] = Field(default=None, primary_key=True)
    food_id: Optional[int] = Field(default=None, foreign_key="human_foods.food_id")
    ingredient_id: Optional[int] = Field(default=None, foreign_key="feed_ingredients.ingredient_id")
    season: str
    yield_kg: float


class ProcessingLossFactor(SQLModel, table=True):
    __tablename__ = "processing_loss_factors"
    loss_id: Optional[int] = Field(default=None, primary_key=True)
    food_id: Optional[int] = Field(default=None, foreign_key="human_foods.food_id")
    ingredient_id: Optional[int] = Field(default=None, foreign_key="feed_ingredients.ingredient_id")
    process: str
    loss_factor: float
=======
    source: Optional[str] = None
    nutrients: Dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    cap: Optional[float] = None


class Nutrient(SQLModel, table=True):
    __tablename__ = "nutrients"
    nutrient_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str


class YieldForecast(SQLModel, table=True):
    __tablename__ = "yield_forecasts"
    forecast_id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="stock_batches.batch_id")
    forecast_time: datetime = Field(default_factory=datetime.utcnow)
    expected_harvest_date: Optional[date] = None
    expected_yield_kg: Optional[float] = None
    yield_std_kg: Optional[float] = None


class AdjustmentLog(SQLModel, table=True):
    __tablename__ = "adjustment_logs"
    adjustment_id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="stock_batches.batch_id")
    field_name: str
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
=======
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
