# Aquaponics Calculator

This repository hosts the early specification work for an aquaculture / aquaponics management application. The project aims to track water chemistry, operational data, feed efficiency, and system hardware to support efficient and sustainable production.

## Database Schema

The initial database schema is defined in [`schema.sql`](schema.sql). It models:

- Species and stock batches
- Water chemistry readings and targets
- Feeding plans and feed logs
- Growth records for performance tracking
- System hardware inventory and maintenance logs
- Operational events and sensor metadata

## Sensor Integration Plan

The schema supports both automated sensor readings and manual data entry. Key priorities:

1. **Tier 1 (Real-time sensors)**: pH, temperature, dissolved oxygen, salinity/conductivity, flow/pump status.
2. **Tier 2 (Semi-automated)**: Ammonia, nitrite, nitrate (sensors if available; otherwise manual logs).
3. **Tier 3 (Manual-only)**: Alkalinity, hardness, phosphate and other maintenance events.

Future development will expand this schema and add application logic for dashboards, alerts, and analytics.

## Analytics Library

The `aquaponics` package implements a set of reference algorithms for common aquaculture calculations, including:

- Hampel outlier filtering and exponential moving averages
- NH₃ fraction and dissolved oxygen saturation estimators
- Nitrification capacity with Q10 temperature correction
- Thermal Growth Coefficient weight projections
- Continuous stirred tank reactor mixing model
- A minimal rule engine for generating threshold-based alerts

Unit tests for these functions are located in the `tests` directory.
