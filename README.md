# BioCargo - Synthetic Biology Cargo Viability Tracker

AI-assisted monitoring of temperature-sensitive biological cargo during flight delays.

## Architecture

```text
Streamlit Dashboard (dashboard.py)
            |
            v
      Flask Backend (app.py)
            |
      +-----+------+
      |            |
      v            v
Prediction      MySQL
  Layer        Database
      |
  +---+---+
  |       |
  v       v
Arrhenius  Random Forest ML
Model      Model
```

## Main files

- `dashboard.py` - Streamlit frontend and dashboard.
- `app.py` - Flask backend/API.
- `prediction.py` - Integrates Arrhenius and ML predictions.
- `viability.py` - Arrhenius-inspired degradation, viability, risk and safe-time calculations.
- `ml_model.py` - Random Forest regression model.
- `generate_dataset.py` - Generates synthetic training data.
- `train_ml.py` - Trains and evaluates the ML model.
- `database.py` - MySQL CRUD operations.
- `models.py` - Cargo data model.
- `schema.sql` - MySQL database/table definition.
- `styles.css` / `components.html` - Earlier standalone UI assets.

## Prediction inputs

The integrated prediction API uses:

- Cargo type
- Current temperature
- Flight duration (hours)
- Flight delay (minutes)

Total exposure time is:

`flight duration + flight delay / 60`

The Arrhenius model then estimates viability and remaining time until the 70% viability threshold.

## Important prototype assumption

The activation energy and baseline decay rate are demonstration parameters. The ML training dataset is synthetic and generated from the Arrhenius-inspired model. Real deployment would require cargo-specific experimental stability data and historical shipment data for calibration and validation.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create the MySQL database/table using `schema.sql`.

3. Check the MySQL connection settings in `database.py`.

4. Generate/rebuild the ML dataset:

```bash
python generate_dataset.py
```

5. Check the ML model:

```bash
python train_ml.py
```

6. Start the Flask backend in one terminal:

```bash
python app.py
```

7. Start the Streamlit dashboard in another terminal:

```bash
streamlit run dashboard.py
```

Open the Streamlit address shown in the terminal.

## API endpoints

- `GET /` - backend health check
- `POST /predict` - calculate a prediction without saving cargo
- `GET /cargo` - list cargo
- `GET /cargo/<cargo_id>` - retrieve one cargo
- `POST /cargo` - create cargo and calculate/save its prediction
- `PUT /cargo/<cargo_id>` - update temperature/delay/duration and recalculate prediction
- `DELETE /cargo/<cargo_id>` - delete cargo
