import mysql.connector
from mysql.connector import Error
from models import Cargo


# =========================================================
# DATABASE CONNECTION
# =========================================================
def get_connection():

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9677149851",
            database="synthetic_cargo"
        )

        return connection

    except Error as error:

        print("Database connection error:", error)
        return None


# =========================================================
# CREATE - ADD CARGO
# =========================================================
def add_cargo(cargo):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            INSERT INTO Cargo (
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            cargo.cargo_id,
            cargo.cargo_type,
            cargo.current_temp,
            cargo.safe_temp,
            cargo.max_temp_threshold,
            cargo.flight_delay_minutes,
            cargo.viability_percentage,
            cargo.risk_level,
            cargo.flight_duration_hours
        )

        cursor.execute(query, values)
        connection.commit()

        return True

    except Error as error:

        print("Error adding cargo:", error)
        connection.rollback()
        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# READ - GET ALL CARGO
# =========================================================
def get_all_cargo():

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:

        query = """
            SELECT
                cargo_id,
                cargo_type,
                current_temp,
                safe_temp,
                max_temp_threshold,
                flight_delay_minutes,
                viability_percentage,
                risk_level,
                flight_duration_hours
            FROM Cargo
        """

        cursor.execute(query)

        records = cursor.fetchall()

        cargo_list = []

        for record in records:

            cargo = Cargo(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5],
                record[6],
                record[7],
                record[8]
            )

            cargo_list.append(cargo)

        return cargo_list

    except Error as error:

        print("Error retrieving cargo:", error)
        return []

    finally:

        cursor.close()
        connection.close()


# =========================================================
# READ - GET ONE CARGO
# =========================================================
def get_cargo(cargo_id):

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:

        query = """
            SELECT
                cargo_id,
                cargo_type,
                current_temp,
                safe_temp,
                max_temp_threshold,
                flight_delay_minutes,
                viability_percentage,
                risk_level,
                flight_duration_hours
            FROM Cargo
            WHERE cargo_id = %s
        """

        cursor.execute(query, (cargo_id,))

        record = cursor.fetchone()

        if record is None:
            return None

        cargo = Cargo(
            record[0],
            record[1],
            record[2],
            record[3],
            record[4],
            record[5],
            record[6],
            record[7],
            record[8]
        )

        return cargo

    except Error as error:

        print("Error retrieving cargo:", error)
        return None

    finally:

        cursor.close()
        connection.close()


# =========================================================
# UPDATE - TEMPERATURE AND DELAY
# =========================================================
def update_cargo(
    cargo_id,
    current_temp,
    flight_delay_minutes
):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            UPDATE Cargo
            SET current_temp = %s,
                flight_delay_minutes = %s
            WHERE cargo_id = %s
        """

        values = (
            current_temp,
            flight_delay_minutes,
            cargo_id
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount > 0

    except Error as error:

        print("Error updating cargo:", error)
        connection.rollback()
        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# DELETE - DELETE CARGO
# =========================================================
def delete_cargo(cargo_id):

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:

        query = """
            DELETE FROM Cargo
            WHERE cargo_id = %s
        """

        cursor.execute(query, (cargo_id,))
        connection.commit()

        return cursor.rowcount > 0

    except Error as error:

        print("Error deleting cargo:", error)
        connection.rollback()
        return False

    finally:

        cursor.close()
        connection.close()


# =========================================================
# TEST DATABASE CONNECTION
# =========================================================
if __name__ == "__main__":

    connection = get_connection()

    if connection is not None and connection.is_connected():

        print("MySQL connected successfully!")

        connection.close()

    else:

        print("MySQL connection failed.")