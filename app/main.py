from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import (
    AdjustmentLog,
    EventLog,
    FeedLog,
    GrowthRecord,
    Ingredient,
    InventorySnapshot,
    Species,
    StockBatch,
    WaterReading,
    WaterTarget,
    YieldForecast,
)
from .optimization import optimize_feed, optimize_menu

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/readings", response_model=WaterReading)
def create_reading(reading: WaterReading, session: Session = Depends(get_session)):
    session.add(reading)
    session.commit()
    session.refresh(reading)

    target = session.exec(
        select(WaterTarget).where(
            WaterTarget.parameter == reading.parameter,
            (WaterTarget.location == reading.location) | (WaterTarget.location == None)
        )
    ).first()
    if target and (reading.value < target.min_value or reading.value > target.max_value):
        event = EventLog(reading_id=reading.reading_id,
                         message=f"{reading.parameter} out of range: {reading.value}")
        session.add(event)
        session.commit()
    return reading

@app.get("/readings")
def list_readings(
    parameter: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    session: Session = Depends(get_session),
):
    stmt = select(WaterReading)
    if parameter:
        stmt = stmt.where(WaterReading.parameter == parameter)
    if start:
        stmt = stmt.where(WaterReading.timestamp >= start)
    if end:
        stmt = stmt.where(WaterReading.timestamp <= end)
    stmt = stmt.order_by(WaterReading.timestamp.desc()).limit(limit)

    readings = session.exec(stmt).all()
    results = []
    for r in readings:
        breach = session.exec(
            select(EventLog).where(EventLog.reading_id == r.reading_id)
        ).first() is not None
        data = r.dict()
        data["breach"] = breach
        results.append(data)
    return results

@app.get("/alerts", response_model=List[EventLog])
def get_alerts(session: Session = Depends(get_session)):
    stmt = select(EventLog).order_by(EventLog.timestamp.desc())
    return session.exec(stmt).all()

@app.get("/fcr")
def calculate_fcr(batch_id: int, session: Session = Depends(get_session)):
    total_feed = session.exec(
        select(FeedLog.amount_g).where(FeedLog.batch_id == batch_id)
    ).all()
    total_feed = sum(total_feed) if total_feed else 0

    weights = session.exec(
        select(GrowthRecord.weight_avg_g)
        .where(GrowthRecord.batch_id == batch_id)
        .order_by(GrowthRecord.timestamp)
    ).all()
    if len(weights) < 2:
        return {"batch_id": batch_id, "fcr": None}
    weight_gain = weights[-1] - weights[0]
    fcr = total_feed / weight_gain if weight_gain else None
    return {"batch_id": batch_id, "fcr": fcr}


class InventoryUpdate(BaseModel):
    ingredient_id: int
    stock_on_hand: float


class ForecastUpdate(BaseModel):
    batch_id: int
    expected_harvest_date: Optional[date] = None
    expected_yield_kg: Optional[float] = None
    yield_std_kg: Optional[float] = None


@app.post("/inventory", response_model=Ingredient)
def update_inventory(update: InventoryUpdate, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, update.ingredient_id)
    if ingredient:
        ingredient.stock_on_hand = update.stock_on_hand
    else:
        ingredient = Ingredient(
            ingredient_id=update.ingredient_id,
            name="unknown",
            stock_on_hand=update.stock_on_hand,
        )
        session.add(ingredient)
    session.add(
        InventorySnapshot(
            ingredient_id=ingredient.ingredient_id,
            stock_on_hand=ingredient.stock_on_hand,
        )
    )
    session.commit()
    session.refresh(ingredient)
    return ingredient


@app.post("/forecasts", response_model=YieldForecast)
def update_forecast(update: ForecastUpdate, session: Session = Depends(get_session)):
    forecast = YieldForecast(
        batch_id=update.batch_id,
        expected_harvest_date=update.expected_harvest_date,
        expected_yield_kg=update.expected_yield_kg,
        yield_std_kg=update.yield_std_kg,
    )
    session.add(forecast)
    batch = session.get(StockBatch, update.batch_id)
    if batch:
        if update.expected_harvest_date and batch.expected_harvest_date != update.expected_harvest_date:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="expected_harvest_date",
                    previous_value=str(batch.expected_harvest_date),
                    new_value=str(update.expected_harvest_date),
                )
            )
            batch.expected_harvest_date = update.expected_harvest_date
        if update.expected_yield_kg is not None and batch.expected_yield_kg != update.expected_yield_kg:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="expected_yield_kg",
                    previous_value=str(batch.expected_yield_kg),
                    new_value=str(update.expected_yield_kg),
                )
            )
            batch.expected_yield_kg = update.expected_yield_kg
        if update.yield_std_kg is not None and batch.yield_std_kg != update.yield_std_kg:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="yield_std_kg",
                    previous_value=str(batch.yield_std_kg),
                    new_value=str(update.yield_std_kg),
                )
            )
            batch.yield_std_kg = update.yield_std_kg
    session.commit()
    session.refresh(forecast)
    return forecast


class IngredientInput(BaseModel):
    name: str
    cost: float = 0
    nutrients: dict


class OptimizationRequest(BaseModel):
    ingredients: List[IngredientInput]
    requirements: dict


@app.post("/optimize/human-menu")
def human_menu(req: OptimizationRequest):
    ingredients = [i.dict() for i in req.ingredients]
    solution = optimize_menu(ingredients, req.requirements)
    return solution


@app.post("/optimize/fish-feed")
def fish_feed(req: OptimizationRequest):
    ingredients = [i.dict() for i in req.ingredients]
    solution = optimize_feed(ingredients, req.requirements)
    return solution
