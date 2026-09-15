import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Features used by the ML model
FEATURES = [
    "cargo_type",
    "current_temp",
    "safe_temp",
    "max_temp_threshold",
    "flight_delay_minutes"
]

TARGET = "viability_percentage"


def train_model(data):
    X = data[FEATURES]
    y = data[TARGET]

    categorical_features = ["cargo_type"]
    numerical_features = [
        "current_temp",
        "safe_temp",
        "max_temp_threshold",
        "flight_delay_minutes"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cargo",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            ),
            (
                "numbers",
                "passthrough",
                numerical_features
            )
        ]
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ))
    ])

    model.fit(X, y)

    return model


def predict_ml(model, cargo_type, current_temp,
               safe_temp, max_temp_threshold,
               flight_delay_minutes):

    input_data = pd.DataFrame([{
        "cargo_type": cargo_type,
        "current_temp": current_temp,
        "safe_temp": safe_temp,
        "max_temp_threshold": max_temp_threshold,
        "flight_delay_minutes": flight_delay_minutes
    }])

    prediction = model.predict(input_data)[0]

    return max(0, min(100, prediction))