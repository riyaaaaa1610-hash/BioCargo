from flask import Flask, request, jsonify

from database import (
    add_cargo,
    get_all_cargo,
    get_cargo,
    update_cargo,
    delete_cargo
)

from models import Cargo
from prediction import get_prediction, CARGO_PARAMETERS


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================
app = Flask(__name__)


# =========================================================
# CONVERT CARGO OBJECT TO JSON
# =========================================================
def cargo_to_dict(cargo):

    return {
        "cargo_id": cargo.cargo_id,
        "cargo_type": cargo.cargo_type,
        "current_temp": cargo.current_temp,
        "safe_temp": cargo.safe_temp,
        "max_temp_threshold": cargo.max_temp_threshold,
        "flight_delay_minutes": cargo.flight_delay_minutes,
        "flight_duration_hours": cargo.flight_duration_hours,
        "viability_percentage": cargo.viability_percentage,
        "risk_level": cargo.risk_level
    }


# =========================================================
# VALIDATE PREDICTION INPUTS
# =========================================================
def validate_prediction_input(data):

    required_fields = [
        "cargo_type",
        "current_temp",
        "flight_duration_hours",
        "flight_delay_minutes"
    ]

    for field in required_fields:
        if field not in data:
            return None, f"Missing required field: {field}"

    cargo_type = str(data["cargo_type"]).strip()

    if cargo_type not in CARGO_PARAMETERS:
        return None, "Unknown cargo type."

    try:
        current_temp = float(data["current_temp"])
        flight_duration_hours = float(data["flight_duration_hours"])
        flight_delay_minutes = int(data["flight_delay_minutes"])
    except (ValueError, TypeError):
        return None, "Invalid numeric value provided."

    if current_temp < -100 or current_temp > 100:
        return None, "Current temperature is outside the accepted range."

    if flight_duration_hours <= 0:
        return None, "Flight duration must be greater than 0."

    if flight_delay_minutes < 0:
        return None, "Flight delay cannot be negative."

    parameters = CARGO_PARAMETERS[cargo_type]

    return {
        "cargo_type": cargo_type,
        "current_temp": current_temp,
        "flight_duration_hours": flight_duration_hours,
        "flight_delay_minutes": flight_delay_minutes,
        "safe_temp": parameters["safe_temp"],
        "max_temp_threshold": parameters["max_temp_threshold"]
    }, None


# =========================================================
# HEALTH CHECK
# =========================================================
@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "Synthetic Cargo Tracker Backend is running!"
    })


# =========================================================
# PREDICT VIABILITY
# =========================================================
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Request must contain JSON data."
        }), 400

    validated, error = validate_prediction_input(data)

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    result = get_prediction(
        cargo_type=validated["cargo_type"],
        current_temp=validated["current_temp"],
        flight_duration_hours=validated["flight_duration_hours"],
        flight_delay_minutes=validated["flight_delay_minutes"]
    )

    return jsonify({
        "success": True,
        "data": {
            **validated,
            **result
        }
    })


# =========================================================
# GET ALL CARGO
# =========================================================
@app.route("/cargo", methods=["GET"])
def get_cargo_list():

    cargo_list = get_all_cargo()

    result = [cargo_to_dict(cargo) for cargo in cargo_list]

    return jsonify({
        "success": True,
        "count": len(result),
        "data": result
    })


# =========================================================
# GET ONE CARGO
# =========================================================
@app.route("/cargo/<cargo_id>", methods=["GET"])
def get_single_cargo(cargo_id):

    cargo = get_cargo(cargo_id)

    if cargo is None:
        return jsonify({
            "success": False,
            "error": "Cargo ID not found."
        }), 404

    return jsonify({
        "success": True,
        "data": cargo_to_dict(cargo)
    })


# =========================================================
# ADD NEW CARGO + CALCULATE PREDICTION
# =========================================================
@app.route("/cargo", methods=["POST"])
def create_cargo():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Request must contain JSON data."
        }), 400

    validated, error = validate_prediction_input(data)

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    cargo_id = str(data.get("cargo_id", "")).strip()

    if cargo_id == "":
        return jsonify({
            "success": False,
            "error": "Cargo ID cannot be empty."
        }), 400

    if get_cargo(cargo_id) is not None:
        return jsonify({
            "success": False,
            "error": "Cargo ID already exists."
        }), 409

    cargo_type = validated["cargo_type"]
    current_temp = validated["current_temp"]
    flight_duration_hours = validated["flight_duration_hours"]
    flight_delay_minutes = validated["flight_delay_minutes"]
    safe_temp = validated["safe_temp"]
    max_temp_threshold = validated["max_temp_threshold"]

    # Run the AI/viability prediction before saving.
    prediction = get_prediction(
        cargo_type=cargo_type,
        current_temp=current_temp,
        flight_duration_hours=flight_duration_hours,
        flight_delay_minutes=flight_delay_minutes
    )

    cargo = Cargo(
        cargo_id,
        cargo_type,
        current_temp,
        safe_temp,
        max_temp_threshold,
        flight_delay_minutes,
        prediction["arrhenius_viability"],
        prediction["risk_level"],
        flight_duration_hours
    )

    if not add_cargo(cargo):
        return jsonify({
            "success": False,
            "error": "Failed to save cargo to database."
        }), 500

    return jsonify({
        "success": True,
        "message": "Cargo added successfully.",
        "data": {
            **cargo_to_dict(cargo),
            **prediction
        }
    }), 201


# =========================================================
# UPDATE CARGO + RECALCULATE PREDICTION
# =========================================================
@app.route("/cargo/<cargo_id>", methods=["PUT"])
def update_single_cargo(cargo_id):

    existing_cargo = get_cargo(cargo_id)

    if existing_cargo is None:
        return jsonify({
            "success": False,
            "error": "Cargo ID not found."
        }), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Request must contain JSON data."
        }), 400

    if "current_temp" not in data:
        return jsonify({
            "success": False,
            "error": "Missing required field: current_temp"
        }), 400

    if "flight_delay_minutes" not in data:
        return jsonify({
            "success": False,
            "error": "Missing required field: flight_delay_minutes"
        }), 400

    if "flight_duration_hours" not in data:
        return jsonify({
            "success": False,
            "error": "Missing required field: flight_duration_hours"
        }), 400

    try:
        current_temp = float(data["current_temp"])
        flight_delay_minutes = int(data["flight_delay_minutes"])
        flight_duration_hours = float(data["flight_duration_hours"])
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Invalid update values."
        }), 400

    if current_temp < -100 or current_temp > 100:
        return jsonify({
            "success": False,
            "error": "Current temperature is outside the accepted range."
        }), 400

    if flight_delay_minutes < 0:
        return jsonify({
            "success": False,
            "error": "Flight delay cannot be negative."
        }), 400

    if flight_duration_hours <= 0:
        return jsonify({
            "success": False,
            "error": "Flight duration must be greater than 0."
        }), 400

    prediction = get_prediction(
        cargo_type=existing_cargo.cargo_type,
        current_temp=current_temp,
        flight_duration_hours=flight_duration_hours,
        flight_delay_minutes=flight_delay_minutes
    )

    if not update_cargo(
        cargo_id,
        current_temp,
        flight_delay_minutes,
        prediction["arrhenius_viability"],
        prediction["risk_level"],
        flight_duration_hours
    ):
        return jsonify({
            "success": False,
            "error": "Failed to update cargo."
        }), 500

    updated_cargo = get_cargo(cargo_id)

    return jsonify({
        "success": True,
        "message": "Cargo updated successfully.",
        "data": {
            **cargo_to_dict(updated_cargo),
            **prediction
        }
    })


# =========================================================
# DELETE CARGO
# =========================================================
@app.route("/cargo/<cargo_id>", methods=["DELETE"])
def delete_single_cargo(cargo_id):

    existing_cargo = get_cargo(cargo_id)

    if existing_cargo is None:
        return jsonify({
            "success": False,
            "error": "Cargo ID not found."
        }), 404

    if not delete_cargo(cargo_id):
        return jsonify({
            "success": False,
            "error": "Failed to delete cargo."
        }), 500

    return jsonify({
        "success": True,
        "message": "Cargo deleted successfully."
    })


# =========================================================
# RUN FLASK SERVER
# =========================================================
if __name__ == "__main__":

    print("\n========================================")
    print("   SYNTHETIC CARGO TRACKER BACKEND")
    print("========================================")
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print("========================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
