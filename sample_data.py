from database import (
    get_connection,
    add_cargo as db_add_cargo,
    get_all_cargo,
    get_cargo,
    update_cargo as db_update_cargo,
    delete_cargo as db_delete_cargo
)


# =========================================================
# TEXT VALIDATION
# =========================================================
def get_text(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print("Error: This field cannot be empty.")

        else:
            return value


# =========================================================
# TEMPERATURE VALIDATION
# =========================================================
def get_temperature(prompt):

    while True:

        try:

            value = float(input(prompt))

            if value < -100 or value > 100:

                print(
                    "Error: Please enter a temperature "
                    "between -100 and 100."
                )

            else:

                return value

        except ValueError:

            print("Error: Please enter a valid number.")


# =========================================================
# DELAY VALIDATION
# =========================================================
def get_delay(prompt):

    while True:

        try:

            value = int(input(prompt))

            if value < 0:

                print(
                    "Error: Flight delay cannot be negative."
                )

            else:

                return value

        except ValueError:

            print(
                "Error: Please enter a whole number."
            )


# =========================================================
# FLIGHT DURATION VALIDATION
# =========================================================
def get_flight_duration(prompt):

    while True:

        try:

            value = float(input(prompt))

            if value <= 0:

                print(
                    "Error: Flight duration must be greater than 0."
                )

            else:

                return value

        except ValueError:

            print(
                "Error: Please enter a valid number of hours."
            )


# =========================================================
# CREATE - ADD NEW CARGO
# =========================================================
def add_new_cargo():

    print("\n========== ADD NEW CARGO ==========")

    cargo_id = get_text("Enter Cargo ID: ")

    if get_cargo(cargo_id) is not None:

        print("Error: Cargo ID already exists.")
        return

    cargo_type = get_text("Enter Cargo Type: ")

    current_temp = get_temperature(
        "Enter Current Temperature: "
    )

    safe_temp = get_temperature(
        "Enter Safe Temperature: "
    )

    max_temp_threshold = get_temperature(
        "Enter Maximum Temperature Threshold: "
    )

    if max_temp_threshold < safe_temp:

        print(
            "Error: Maximum temperature threshold "
            "cannot be lower than safe temperature."
        )

        return

    flight_delay_minutes = get_delay(
        "Enter Flight Delay (minutes): "
    )

    flight_duration_hours = get_flight_duration(
        "Enter Flight Duration (hours): "
    )

    # Initial values
    viability_percentage = 100.0
    risk_level = "Safe"

    # Create database object
    from models import Cargo

    cargo = Cargo(
        cargo_id,
        cargo_type,
        current_temp,
        safe_temp,
        max_temp_threshold,
        flight_delay_minutes,
        viability_percentage,
        risk_level,
        flight_duration_hours
    )

    if db_add_cargo(cargo):

        print("\nCargo added successfully!")

    else:

        print("\nFailed to add cargo.")


# =========================================================
# READ - VIEW ALL CARGO
# =========================================================
def view_cargo():

    print("\n========== CARGO RECORDS ==========")

    cargo_list = get_all_cargo()

    if len(cargo_list) == 0:

        print("No cargo records found.")
        return

    for cargo in cargo_list:

        print("--------------------------------")

        print("Cargo ID:", cargo.cargo_id)
        print("Cargo Type:", cargo.cargo_type)
        print("Current Temperature:",
              cargo.current_temp)
        print("Safe Temperature:",
              cargo.safe_temp)
        print("Maximum Temperature Threshold:",
              cargo.max_temp_threshold)
        print("Flight Delay:",
              cargo.flight_delay_minutes,
              "minutes")
        print("Flight Duration:",
              cargo.flight_duration_hours,
              "hours")
        print("Viability:",
              cargo.viability_percentage,
              "%")
        print("Risk Level:",
              cargo.risk_level)


# =========================================================
# UPDATE CARGO
# =========================================================
def update_existing_cargo():

    print("\n========== UPDATE CARGO ==========")

    cargo_id = get_text("Enter Cargo ID: ")

    if get_cargo(cargo_id) is None:

        print("Error: Cargo ID not found.")
        return

    current_temp = get_temperature(
        "Enter New Current Temperature: "
    )

    flight_delay_minutes = get_delay(
        "Enter New Flight Delay (minutes): "
    )

    if db_update_cargo(
        cargo_id,
        current_temp,
        flight_delay_minutes
    ):

        print("\nCargo updated successfully!")

    else:

        print("\nCargo update failed.")


# =========================================================
# DELETE CARGO
# =========================================================
def delete_existing_cargo():

    print("\n========== DELETE CARGO ==========")

    cargo_id = get_text(
        "Enter Cargo ID to delete: "
    )

    if get_cargo(cargo_id) is None:

        print("Error: Cargo ID not found.")
        return

    confirmation = input(
        "Are you sure you want to delete this cargo? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print("Delete cancelled.")
        return

    if db_delete_cargo(cargo_id):

        print("\nCargo deleted successfully!")

    else:

        print("\nCargo deletion failed.")


# =========================================================
# MAIN MENU
# =========================================================
if __name__ == "__main__":

    while True:

        print("\n========================================")
        print("      SYNTHETIC CARGO TRACKER")
        print("========================================")

        print("1. Add Cargo")
        print("2. View Cargo")
        print("3. Update Cargo")
        print("4. Delete Cargo")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            add_new_cargo()

        elif choice == "2":

            view_cargo()

        elif choice == "3":

            update_existing_cargo()

        elif choice == "4":

            delete_existing_cargo()

        elif choice == "5":

            print("\nExiting Synthetic Cargo Tracker...")
            break

        else:

            print("Invalid choice. Please select 1-5.")