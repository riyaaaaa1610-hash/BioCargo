class Cargo:

    def __init__(
        self,
        cargo_id,
        cargo_type,
        current_temp,
        safe_temp,
        max_temp_threshold,
        flight_delay_minutes,
        viability_percentage,
        risk_level,
        flight_duration_hours
    ):
        self.cargo_id = cargo_id
        self.cargo_type = cargo_type
        self.current_temp = current_temp
        self.safe_temp = safe_temp
        self.max_temp_threshold = max_temp_threshold
        self.flight_delay_minutes = flight_delay_minutes
        self.viability_percentage = viability_percentage
        self.risk_level = risk_level
        self.flight_duration_hours = flight_duration_hours

    def display(self):

        print("\n========== CARGO DETAILS ==========")
        print("Cargo ID:", self.cargo_id)
        print("Cargo Type:", self.cargo_type)
        print("Current Temperature:", self.current_temp)
        print("Safe Temperature:", self.safe_temp)
        print("Maximum Temperature Threshold:",
              self.max_temp_threshold)
        print("Flight Delay:",
              self.flight_delay_minutes, "minutes")
        print("Flight Duration:",
              self.flight_duration_hours, "hours")
        print("Viability:",
              self.viability_percentage, "%")
        print("Risk Level:",
              self.risk_level)