from typing import List
import httpx
from sqlmodel import Session

from .models import Ingredient, StockBatch, YieldForecast, AdjustmentLog, InventorySnapshot


async def pull_current_stocks(api_url: str) -> List[dict]:
    """Fetch current stock levels from an external service."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(api_url)
        resp.raise_for_status()
        return resp.json()


async def pull_les_yield_forecasts(api_url: str) -> List[dict]:
    """Fetch LES yield forecasts from an external service."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(api_url)
        resp.raise_for_status()
        return resp.json()


async def ingest_inventory(stock_url: str, session: Session) -> None:
    """Update ingredient stock levels from a remote source."""
    stocks = await pull_current_stocks(stock_url)
    for item in stocks:
        ingredient = session.get(Ingredient, item["ingredient_id"])
        if ingredient:
            ingredient.stock_on_hand = item["stock_on_hand"]
            session.add(
                InventorySnapshot(
                    ingredient_id=ingredient.ingredient_id,
                    stock_on_hand=ingredient.stock_on_hand,
                )
            )
    session.commit()


async def ingest_forecasts(forecast_url: str, session: Session) -> None:
    """Store yield forecasts and update batch metadata."""
    forecasts = await pull_les_yield_forecasts(forecast_url)
    for item in forecasts:
        forecast = YieldForecast(
            batch_id=item["batch_id"],
            expected_harvest_date=item.get("expected_harvest_date"),
            expected_yield_kg=item.get("expected_yield_kg"),
            yield_std_kg=item.get("yield_std_kg"),
        )
        session.add(forecast)

        batch = session.get(StockBatch, item["batch_id"])
        if not batch:
            continue

        if forecast.expected_harvest_date and batch.expected_harvest_date != forecast.expected_harvest_date:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="expected_harvest_date",
                    previous_value=str(batch.expected_harvest_date),
                    new_value=str(forecast.expected_harvest_date),
                )
            )
            batch.expected_harvest_date = forecast.expected_harvest_date

        if forecast.expected_yield_kg is not None and batch.expected_yield_kg != forecast.expected_yield_kg:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="expected_yield_kg",
                    previous_value=str(batch.expected_yield_kg),
                    new_value=str(forecast.expected_yield_kg),
                )
            )
            batch.expected_yield_kg = forecast.expected_yield_kg

        if forecast.yield_std_kg is not None and batch.yield_std_kg != forecast.yield_std_kg:
            session.add(
                AdjustmentLog(
                    batch_id=batch.batch_id,
                    field_name="yield_std_kg",
                    previous_value=str(batch.yield_std_kg),
                    new_value=str(forecast.yield_std_kg),
                )
            )
            batch.yield_std_kg = forecast.yield_std_kg

    session.commit()
