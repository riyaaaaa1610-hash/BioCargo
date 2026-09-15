from viability import predict_viability
from ml_model import train_model, predict_ml
import pandas as pd


CARGO_PARAMETERS = {

    "Solid Organs": {
        "safe_temp": 5,
        "max_temp_threshold": 8,
    },

    "Platelets": {
        "safe_temp": 22,
        "max_temp_threshold": 24,
    },

    "Red Blood Cells": {
        "safe_temp": 5,
        "max_temp_threshold": 10,
    },

    "Plasma & Cryo": {
        "safe_temp": -18,
        "max_temp_threshold": -18,
    },

    "Skin, Bones, Valves": {
        "safe_temp": -40,
        "max_temp_threshold": -40,
    }
}


DEFAULT_DECAY_RATE = 0.02


# Load training data and train the ML model
data = pd.read_csv("training_data.csv")
ml_model = train_model(data)


def get_prediction(
    cargo_type,
    current_temp,
    flight_delay_minutes
):
    """
    Get Arrhenius and ML viability predictions based on cargo type.
    """

    if cargo_type not in CARGO_PARAMETERS:
        raise ValueError("Unknown cargo type")

    parameters = CARGO_PARAMETERS[cargo_type]

    # -----------------------------
    # Arrhenius prediction
    # -----------------------------
    arrhenius_result = predict_viability(
        current_temp=current_temp,
        safe_temp=parameters["safe_temp"],
        max_temp_threshold=parameters["max_temp_threshold"],
        flight_delay_minutes=flight_delay_minutes,
        decay_rate=DEFAULT_DECAY_RATE
    )

    # -----------------------------
    # ML prediction
    # -----------------------------
    ml_viability = predict_ml(
        model=ml_model,
        cargo_type=cargo_type,
        current_temp=current_temp,
        safe_temp=parameters["safe_temp"],
        max_temp_threshold=parameters["max_temp_threshold"],
        flight_delay_minutes=flight_delay_minutes
    )

    # Add ML prediction to the existing Arrhenius results
    result = {
        "arrhenius_viability": arrhenius_result["viability_percentage"],
        "ml_viability": round(ml_viability, 2),

        "risk_level": arrhenius_result["risk_level"],
        "temperature_status": arrhenius_result["temperature_status"],
        "time_remaining_hours": arrhenius_result["time_remaining_hours"],
        "degradation_rate": arrhenius_result["degradation_rate"]
    }

    return result


if __name__ == "__main__":

    result = get_prediction(
        cargo_type="Solid Organs",
        current_temp=7,
        flight_delay_minutes=600
    )

    print(result)