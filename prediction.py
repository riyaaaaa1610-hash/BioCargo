from viability import predict_viability

DEFAULT_DECAY_RATE = 0.02


def get_prediction(
    current_temp,
    safe_temp,
    max_temp_threshold,
    flight_delay_minutes
):
    """
    Get viability prediction using the default decay rate.
    """

    result = predict_viability(
        current_temp=current_temp,
        safe_temp=safe_temp,
        max_temp_threshold=max_temp_threshold,
        flight_delay_minutes=flight_delay_minutes,
        decay_rate=DEFAULT_DECAY_RATE
    )

    return result


if __name__ == "__main__":

    result = get_prediction(
    current_temp=5,
    safe_temp=5,
    max_temp_threshold=8,
    flight_delay_minutes=1200
)

    print(result)
