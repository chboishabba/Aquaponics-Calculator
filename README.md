# Aquaponics Calculator

This repository hosts the early specification work for an aquaculture / aquaponics management application. The initial FastAPI implementation provides a thin slice of functionality to build on.

## Roadmap

A high-level roadmap illustrating planned phases and data flow between the nutrient databases, optimizers and LES is available in [docs/roadmap.md](docs/roadmap.md).

## Database Schema

The initial database schema is defined in [`schema.sql`](schema.sql) and modeled in the application with SQLModel.

## Getting Started

```bash
pip install -r requirements.txt
python -m app.seed  # create database and seed defaults
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` for a minimal dashboard. A background simulator can post demo readings:

```bash
python -m app.sensor_sim
```

## API Endpoints

- `POST /readings` – add a new water reading
- `GET /readings` – list readings with optional filters
- `GET /alerts` – current alert events
- `GET /fcr?batch_id=1` – calculate Feed Conversion Ratio for a batch

This small slice runs end‑to‑end and can be extended with additional parameters, sensors and KPIs.

## Home Assistant Blueprint

A reusable automation blueprint for temperature‑keyed dissolved oxygen control is available under
[`homeassistant/blueprints/aquaponics/temp_keyed_do_control.yaml`](homeassistant/blueprints/aquaponics/temp_keyed_do_control.yaml).
It adjusts aeration based on DO percent saturation, water temperature and recent feeding events with
configurable gains, deadband and minimum cycle protection.

An auxiliary blueprint, [`homeassistant/blueprints/aquaponics/feeding_activity_monitor.yaml`](homeassistant/blueprints/aquaponics/feeding_activity_monitor.yaml),
toggles a *recent feeding* flag for a configurable window whenever the feeder switch turns on.

## Documentation

- [AI architecture overview](docs/ai_architecture.md)
