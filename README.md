# 🌱 Aquaponics-Calculator

**Part of the Living Environment Simulation Platform**  
> *An open-source, analytics-driven toolkit for managing aquaponics and aquaculture systems — from backyard setups to commercial farms — designed to integrate into a broader real-time environmental modelling ecosystem.*

## Roadmap

A high-level roadmap illustrating planned phases and data flow between the nutrient databases, optimizers and LES is available in [docs/roadmap.md](docs/roadmap.md).

## Database Schema


## 📖 Overview

The **Aquaponics-Calculator** is a **modular, API-first management tool** that tracks water chemistry, stock performance, feeding, growth, and system health for aquaponics and aquaculture.  
It is built to be:

- **Open** – free and extensible for DIY, research, and commercial use.
- **Sensor-agnostic** – works with any IoT hardware, manual entries, or simulated inputs.
- **Analytics-driven** – not just logging, but computing KPIs, forecasts, and nutrient balances.
- **Scalable** – one tank or an entire facility, multiple sites, multiple species.

The project is a **component** of our larger **Living Environment Simulation Platform** — a modular system that couples biological growth, climate, hydrology, erosion, and ecology into a unified simulation + control layer.

---

## ✨ Features

### Core (v0.1 target)
- 📊 **Relational Data Model** – species, stock batches, water readings, feed logs, growth records, hardware, events.
- ⚠️ **Alerts Engine** – threshold & rate-of-change alerts for pH, DO, temperature, etc.
- 🐟 **Key KPIs** – FCR, specific growth rate, survival %, condition factor.
- 🧮 **Nutrient Load Calculator** – TAN production, NH₃ toxicity (pH/temp-aware).
- 💧 **DO % Saturation Calculator** – temp/salinity-corrected, dynamic setpoints.
- 🔌 **Sensor Simulator** – feed the system with realistic demo data for testing.
- 🌐 **API-First** – REST endpoints for all core entities.

### Planned (v0.2+)
- 📈 **Forecasting** – Holt-Winters/STL for pH/temp/DO; TGC-based growth projections.
- 🔄 **Automation Hooks** – integrate with Home Assistant, Node-RED, or direct MQTT for aeration, dosing, feeding.
- 🪴 **Aquaponics Nutrient Balance** – plant uptake vs. fish waste, deficit alerts.
- 🧬 **Genetics & Stock Management** – pedigree, breeding performance.
- 🗺 **Multi-Site Support** – group tanks by facility with per-site targets.
- 📱 **Web Dashboard** – responsive charts, alerts, KPI panels.
- 📤 **Data Export** – CSV/JSON for external analysis or regulatory reporting.

---

## 🔍 Comparison to Other Open-Source Tools

| Feature / Focus              | **Aquaponics-Calculator** | **AquaPi (ESPHome)** | **Open Aquarium** | **Piponics** | **Reef-Pi** |
|------------------------------|---------------------------|----------------------|-------------------|--------------|-------------|
| **Core purpose**              | Analytics + mgmt          | Sensor automation    | DIY automation    | Pi + cloud   | Reef tank control |
| **Data model (stocks, feed)** | ✅                        | ❌                   | ❌                | ❌           | ❌          |
| **KPIs & forecasting**        | ✅                        | ❌                   | ❌                | ❌           | ❌          |
| **Sensor agnostic**           | ✅                        | ⚠️ (ESP only)        | ⚠️ (Arduino)      | ❌           | ❌          |
| **Automation hooks**          | Planned                   | ✅                   | ✅                | ❌           | ✅          |
| **Multi-site scaling**        | ✅                        | ❌                   | ❌                | ❌           | ❌          |
| **Nutrient balance**          | Planned                   | ❌                   | ❌                | ❌           | ❌          |
| **Genetics tracking**         | Planned                   | ❌                   | ❌                | ❌           | ❌          |
| **Open-source**                | ✅                        | ✅                   | ✅                | ✅           | ✅          |

---

## 🗺 Roadmap

**v0.1 – MVP** *(2–3 weeks)*  
- Core DB schema + migrations.  
- REST API for species, batches, readings, targets, feed logs.  
- Basic alert engine (threshold).  
- FCR, SGR, survival calculations.  
- DO % sat + NH₃ toxicity calculators.  
- Simulated sensor feed.  
- Minimal HTML dashboard with readings + alerts.

**v0.2 – Automation & Forecasting**  
- Weather/temp-compensated DO targets.  
- Forecasting (Holt-Winters, TGC growth).  
- Aquaponics nutrient balance.  
- Home Assistant / MQTT control integration.

**v0.3 – Advanced Management**  
- Genetics & breeding records.  
- Multi-site facility management.  
- Advanced alert rules (EWMA, rate-of-change).  
- Role-based user management.

**v1.0 – Full Integration**  
- Web SPA dashboard.  
- External API connectors (e.g., Living Environment Platform).  
- Automated optimisation routines (feeding, aeration, dosing).  
- Data export/import for regulatory compliance.

---

## 🛠 Tech Stack (planned)
- **Backend:** Python + FastAPI + SQLModel/Alembic.
- **DB:** SQLite (dev), PostgreSQL (prod).
- **Frontend:** Minimal HTML/JS for MVP → React/Svelte for v1.
- **Integrations:** MQTT, Home Assistant, Node-RED.
- **CI/CD:** GitHub Actions, pytest, black, ruff.

---

## 🤝 Contributing
We welcome contributions from aquaculture practitioners, makers, and developers.  
Issues & PRs are open — please discuss new modules or analytics before coding.

---

## 📜 License
MIT License – see [LICENSE](LICENSE) for details.

---

**Aquaponics-Calculator** is one piece of the larger *Living Environment Simulation Platform*, which aims to couple detailed biological, environmental, and climatic processes into a unified, scalable, real-time simulation and management framework.

---

This small slice runs end‑to‑end and can be extended with additional parameters, sensors and KPIs.

## Home Assistant Blueprint

A reusable automation blueprint for temperature‑keyed dissolved oxygen control is available under
[`homeassistant/blueprints/aquaponics/temp_keyed_do_control.yaml`](homeassistant/blueprints/aquaponics/temp_keyed_do_control.yaml).
It adjusts aeration based on DO percent saturation, water temperature and recent feeding events with
configurable gains, deadband and minimum cycle protection.

An auxiliary blueprint, [`homeassistant/blueprints/aquaponics/feeding_activity_monitor.yaml`](homeassistant/blueprints/aquaponics/feeding_activity_monitor.yaml),
toggles a *recent feeding* flag for a configurable window whenever the feeder switch turns on.

## Analytics Library

The `aquaponics` package implements a set of reference algorithms for common aquaculture calculations, including:

- Hampel outlier filtering and exponential moving averages
- NH₃ fraction and dissolved oxygen saturation estimators
- Nitrification capacity with Q10 temperature correction
- Thermal Growth Coefficient weight projections
- Continuous stirred tank reactor mixing model
- A minimal rule engine for generating threshold-based alerts

Unit tests for these functions are located in the `tests` directory.

## Documentation


## Analytics Library

The `aquaponics` package implements a set of reference algorithms for common aquaculture calculations, including:

- Hampel outlier filtering and exponential moving averages
- NH₃ fraction and dissolved oxygen saturation estimators
- Nitrification capacity with Q10 temperature correction
- Thermal Growth Coefficient weight projections
- Continuous stirred tank reactor mixing model
- A minimal rule engine for generating threshold-based alerts

Unit tests for these functions are located in the `tests` directory.

- [AI architecture overview](docs/ai_architecture.md)

