import math


# Gas constant
R = 8.314  # J/(mol·K)

# Activation energy
# DEMO VALUE - should be replaced with validated cargo-specific data
DEFAULT_EA = 50000  # J/mol

# Viability threshold below which cargo is considered critical
CRITICAL_VIABILITY = 70.0


def celsius_to_kelvin(temperature_c):
    """
    Convert temperature from Celsius to Kelvin.
    """
    return temperature_c + 273.15


def calculate_degradation_rate(
    current_temp,
    safe_temp,
    decay_rate,
    activation_energy=DEFAULT_EA
):
    """
    Calculate temperature-adjusted degradation rate
    using an Arrhenius-inspired model.
    """

    current_temp_k = celsius_to_kelvin(current_temp)
    safe_temp_k = celsius_to_kelvin(safe_temp)

    rate = decay_rate * math.exp(
        (activation_energy / R) *
        ((1 / safe_temp_k) - (1 / current_temp_k))
    )

    return rate


def calculate_viability(degradation_rate, elapsed_hours):
    """
    Calculate remaining biological viability.
    """

    viability = 100 * math.exp(
        -degradation_rate * elapsed_hours
    )

    return max(0.0, min(100.0, viability))


def calculate_safe_time(
    degradation_rate,
    elapsed_hours,
    threshold=CRITICAL_VIABILITY
):
    """
    Calculate the estimated remaining time
    before viability reaches the critical threshold.
    """

    if degradation_rate <= 0:
        return float("inf")

    total_safe_time = (
        -math.log(threshold / 100)
        / degradation_rate
    )

    remaining_time = total_safe_time - elapsed_hours

    return max(0.0, remaining_time)


def classify_risk(viability):
    """
    Classify cargo based on remaining viability.
    """

    if viability >= 90:
        return "Safe"

    elif viability >= 70:
        return "Warning"

    else:
        return "Critical"

def check_temperature(current_temp, safe_temp, max_temp_threshold):
    """
    Check whether the current temperature is within
    the defined safe temperature range.
    """

    if current_temp <= safe_temp:
        return "Safe"

    elif current_temp <= max_temp_threshold:
        return "Warning"

    else:
        return "Above Safe Limit"

def predict_viability(
    current_temp,
    safe_temp,
    max_temp_threshold,
    flight_duration_hours,
    flight_delay_minutes,
    decay_rate
):
    """
    Main viability prediction function.
    """

    # Convert delay from minutes to hours
    total_exposure_hours = flight_duration_hours + (flight_delay_minutes / 60)

    # Calculate temperature-adjusted degradation
    degradation_rate = calculate_degradation_rate(
        current_temp,
        safe_temp,
        decay_rate
    )

    # Calculate current viability
    viability_percentage = calculate_viability(
        degradation_rate,
        total_exposure_hours
    )

    # Calculate remaining safe time
    safe_time = calculate_safe_time(
        degradation_rate,
        total_exposure_hours
    )

    # Check temperature against thresholds
    temperature_status = check_temperature(
        current_temp,
        safe_temp,
        max_temp_threshold
    )

    # Calculate risk based on viability
    risk_level = classify_risk(viability_percentage)

    return {
        "viability_percentage": round(viability_percentage, 2),
        "degradation_rate": round(degradation_rate, 6),
        "time_remaining_hours": round(safe_time, 2),
        "total_exposure_hours": round(total_exposure_hours,2),
        "risk_level": risk_level,
        "temperature_status": temperature_status
    }

if __name__ == "__main__":

    test_cases = [

    # 10-hour delay
    {
        "current_temp": 5,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600,
        "decay_rate": 0.02
    },

    {
        "current_temp": 7,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600,
        "decay_rate": 0.02
    },

    {
        "current_temp": 10,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 600,
        "decay_rate": 0.02
    },

    # 20-hour delay
    {
        "current_temp": 5,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 1200,
        "decay_rate": 0.02
    },

    {
        "current_temp": 7,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 1200,
        "decay_rate": 0.02
    },

    {
        "current_temp": 10,
        "safe_temp": 5,
        "max_temp_threshold": 8,
        "flight_duration_hours": 8,
        "flight_delay_minutes": 1200,
        "decay_rate": 0.02
    }
]

    for case in test_cases:
        result = predict_viability(**case)
        print(case)
        print(result)
        print("-" * 50)
