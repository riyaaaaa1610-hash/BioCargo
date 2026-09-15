import pandas as pd
from ml_model import train_model, predict_ml
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


data = pd.read_csv("training_data.csv")


X = data[
    [
        "cargo_type",
        "current_temp",
        "safe_temp",
        "max_temp_threshold",
        "flight_duration_hours",
        "flight_delay_minutes"
    ]
]

y = data["viability_percentage"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


train_data = X_train.copy()
train_data["viability_percentage"] = y_train


model = train_model(train_data)


predictions = model.predict(X_test)


mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("Model Evaluation")
print("----------------")
print("MAE:", round(mae, 2))
print("R²:", round(r2, 3))


print("\nExample Prediction")
print("------------------")


prediction = predict_ml(
    model=model,
    cargo_type="Solid Organs",
    current_temp=7,
    safe_temp=5,
    max_temp_threshold=8,
    flight_duration_hours=8,
    flight_delay_minutes=600
)


print("Cargo Type: Solid Organs")
print("Temperature: 7°C")
print("Flight Duration: 8 hours")
print("Flight Delay: 600 minutes")
print("ML Predicted Viability:", round(prediction, 2), "%")


test_cases = [

    {
        "cargo_type": "Solid Organs",
        "current_temp": 5,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600
    },

    {
        "cargo_type": "Solid Organs",
        "current_temp": 7,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600
    },

    {
        "cargo_type": "Solid Organs",
        "current_temp": 10,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600
    },

    {
        "cargo_type": "Solid Organs",
        "current_temp": 7,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 1200
    }
]


print("\nMultiple Test Cases")
print("-------------------")


for case in test_cases:

    result = predict_ml(
        model=model,
        cargo_type=case["cargo_type"],
        current_temp=case["current_temp"],
        safe_temp=case["safe_temp"],
        max_temp_threshold=case["max_temp_threshold"],
        flight_duration_hours=case["flight_duration_hours"],
        flight_delay_minutes=case["flight_delay_minutes"]
    )

    print(
        f"Temp: {case['current_temp']}°C | "
        f"Duration: {case['flight_duration_hours']} h | "
        f"Delay: {case['flight_delay_minutes']} min | "
        f"Viability: {result:.2f}%"
    )