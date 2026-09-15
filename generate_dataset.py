import random
import pandas as pd

from viability import (
    calculate_degradation_rate,
    calculate_viability
)


CARGO_PARAMETERS = {
    "Solid Organs": {
        "safe_temp": 5,
        "max_temp_threshold": 8
    },
    "Platelets": {
        "safe_temp": 22,
        "max_temp_threshold": 24
    },
    "Red Blood Cells": {
        "safe_temp": 5,
        "max_temp_threshold": 10
    }
}


rows = []

for cargo_type, params in CARGO_PARAMETERS.items():

    for _ in range(300):

        current_temp = random.uniform(
            params["safe_temp"] - 2,
            params["max_temp_threshold"] + 4
        )

        flight_delay_minutes = random.randint(0, 1440)

        decay_rate = 0.02

        degradation_rate = calculate_degradation_rate(
            current_temp,
            params["safe_temp"],
            decay_rate
        )

        elapsed_hours = flight_delay_minutes / 60

        viability = calculate_viability(
            degradation_rate,
            elapsed_hours
        )

        rows.append({
            "cargo_type": cargo_type,
            "current_temp": round(current_temp, 2),
            "safe_temp": params["safe_temp"],
            "max_temp_threshold": params["max_temp_threshold"],
            "flight_delay_minutes": flight_delay_minutes,
            "viability_percentage": round(viability, 2)
        })


df = pd.DataFrame(rows)

df.to_csv("training_data.csv", index=False)

print("Training dataset created!")
print(df.head())
print("Total records:", len(df))