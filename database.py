import os

from dotenv import load_dotenv
import mysql.connector

load_dotenv()
from mysql.connector import Error

from models import Cargo


def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE", "synthetic_cargo"),
        )
    except Error as error:
        print("Database connection error:", error)
        return None


def add_cargo(cargo):
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO Cargo (
                cargo_id, cargo_type, current_temp, safe_temp,
                max_temp_threshold, flight_delay_minutes,
                viability_percentage, risk_level, flight_duration_hours
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            cargo.cargo_id, cargo.cargo_type, cargo.current_temp,
            cargo.safe_temp, cargo.max_temp_threshold,
            cargo.flight_delay_minutes, cargo.viability_percentage,
            cargo.risk_level, cargo.flight_duration_hours,
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


def _cargo_from_record(record):
    if record is None:
        return None
    return Cargo(
        record[0], record[1], record[2], record[3], record[4],
        record[5], record[6], record[7], record[8]
    )


def get_all_cargo():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT cargo_id, cargo_type, current_temp, safe_temp,
                   max_temp_threshold, flight_delay_minutes,
                   viability_percentage, risk_level, flight_duration_hours
            FROM Cargo ORDER BY cargo_id
        """)
        return [_cargo_from_record(record) for record in cursor.fetchall()]
    except Error as error:
        print("Error retrieving cargo:", error)
        return []
    finally:
        cursor.close()
        connection.close()


def get_cargo(cargo_id):
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT cargo_id, cargo_type, current_temp, safe_temp,
                   max_temp_threshold, flight_delay_minutes,
                   viability_percentage, risk_level, flight_duration_hours
            FROM Cargo WHERE cargo_id = %s
        """, (cargo_id,))
        return _cargo_from_record(cursor.fetchone())
    except Error as error:
        print("Error retrieving cargo:", error)
        return None
    finally:
        cursor.close()
        connection.close()


def update_cargo(cargo_id, current_temp, flight_delay_minutes,
                 viability_percentage=None, risk_level=None,
                 flight_duration_hours=None):
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        if viability_percentage is None or risk_level is None or flight_duration_hours is None:
            query = """
                UPDATE Cargo
                SET current_temp = %s, flight_delay_minutes = %s
                WHERE cargo_id = %s
            """
            values = (current_temp, flight_delay_minutes, cargo_id)
        else:
            query = """
                UPDATE Cargo
                SET current_temp = %s, flight_delay_minutes = %s,
                    flight_duration_hours = %s, viability_percentage = %s,
                    risk_level = %s
                WHERE cargo_id = %s
            """
            values = (current_temp, flight_delay_minutes, flight_duration_hours,
                      viability_percentage, risk_level, cargo_id)
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


def delete_cargo(cargo_id):
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Cargo WHERE cargo_id = %s", (cargo_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error as error:
        print("Error deleting cargo:", error)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    connection = get_connection()
    if connection is not None and connection.is_connected():
        print("MySQL connected successfully!")
        connection.close()
    else:
        print("MySQL connection failed.")
