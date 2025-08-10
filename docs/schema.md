# Database schema and data import

This project models additional concepts needed for diet and feed planning.
The new tables introduced are:

- `source_tags` – identifies the data source for an item and whether it is
  produced on the farm.
- `human_foods` – foods for human consumption sourced from AUSNUT and USDA
  FoodData Central. Each record optionally links to a `source_tags` entry and
  marks `available_on_farm`.
- `feed_ingredients` – ingredients for animal feed. Records may come from
  Feedipedia or aquaculture tables and also link to `source_tags`.
- `seasonal_yields` – expected production in kilograms for a given season for
  a human food or feed ingredient.
- `processing_loss_factors` – fraction of weight lost during processing steps
  such as cleaning or drying.

## Import process

ETL helpers live in `app/etl/`. Each module exposes a `load(session)` function
that reads a CSV file from the `data/` directory and populates the database.
The seed script (`app/seed.py`) calls all loaders after creating the tables.
CSV files are optional; if a file is missing the loader simply skips it.

Example:

```bash
python -m app.seed  # creates tables and loads available datasets
```

CSV files should include at least a `name` column and may include an
`available_on_farm` boolean column to flag local production.
