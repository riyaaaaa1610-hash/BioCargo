from viability import predict_viability


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


def get_prediction(
    cargo_type,
    current_temp,
    flight_delay_minutes
):
    """
    Get viability prediction based on cargo type.
    """

    if cargo_type not in CARGO_PARAMETERS:
        raise ValueError("Unknown cargo type")

    parameters = CARGO_PARAMETERS[cargo_type]

    result = predict_viability(
        current_temp=current_temp,
        safe_temp=parameters["safe_temp"],
        max_temp_threshold=parameters["max_temp_threshold"],
        flight_delay_minutes=flight_delay_minutes,
        decay_rate=DEFAULT_DECAY_RATE
    )

    return result


if __name__ == "__main__":

    result = get_prediction(
        cargo_type="Solid Organs",
        current_temp=7,
        flight_delay_minutes=600
    )

    print(result)