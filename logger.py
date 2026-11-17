import sqlite3
import argparse
import random
import time
from datetime import datetime

try:
    import serial
except ImportError:
    serial = None

DB_NAME = "classroom_env.db"


def init_db():
    """Create the sensor_readings table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recorded_at TEXT NOT NULL,
            station_name TEXT NOT NULL,
            temp_c REAL NOT NULL,
            humidity_pct REAL NOT NULL
        )
    """)
    conn.commit()
    return conn


def insert_reading(conn, station, temp_c, humidity):
    """Validate and insert a single sensor reading into SQLite."""
    if not (-40.0 <= temp_c <= 85.0) or not (0.0 <= humidity <= 100.0):
        print(f"[SKIPPED] Out-of-range values: {temp_c}°C, {humidity}%")
        return

    timestamp = datetime.now().isoformat(timespec="seconds")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_readings (recorded_at, station_name, temp_c, humidity_pct) VALUES (?, ?, ?, ?)",
        (timestamp, station, temp_c, humidity),
    )
    conn.commit()
    print(f"[{timestamp}] {station} | Temp: {temp_c:.2f}°C | Humidity: {humidity:.2f}%")


def print_summary(conn):
    """Query aggregate statistics for classroom data analysis."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            ROUND(AVG(temp_c), 2) as avg_temp,
            ROUND(MIN(temp_c), 2) as min_temp,
            ROUND(MAX(temp_c), 2) as max_temp,
            ROUND(AVG(humidity_pct), 2) as avg_hum
        FROM sensor_readings
    """)
    row = cursor.fetchone()
    if row and row[0] > 0:
        print("\n--- Session Summary Statistics ---")
        print(f"Total Readings : {row[0]}")
        print(f"Temperature    : Avg {row[1]}°C (Min: {row[2]}°C, Max: {row[3]}°C)")
        print(f"Avg Humidity   : {row[4]}%")


def run_logger(port, baud, station, simulate):
    conn = init_db()
    print(f"Logging started for '{station}' (Press Ctrl+C to stop)...\n")

    try:
        if simulate:
            while True:
                temp = round(random.uniform(20.5, 24.5), 2)
                hum = round(random.uniform(40.0, 55.0), 2)
                insert_reading(conn, station, temp, hum)
                time.sleep(2)
        else:
            if serial is None:
                raise RuntimeError("pyserial is not installed. Run: pip install pyserial")
            with serial.Serial(port, baud, timeout=2) as ser:
                while True:
                    line = ser.readline().decode("utf-8").strip()
                    if not line or line.startswith("timestamp") or line.startswith("ERROR"):
                        continue
                    parts = line.split(",")
                    if len(parts) == 3:
                        _, temp_str, hum_str = parts
                        insert_reading(conn, station, float(temp_str), float(hum_str))
    except KeyboardInterrupt:
        print("\nStopping logger...")
        print_summary(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arduino Uno R4 Environmental SQL Logger")
    parser.add_argument("--port", default="COM3", help="Serial port (e.g., COM3 or /dev/ttyACM0)")
    parser.add_argument("--baud", type=int, default=115200, help="Serial baud rate")
    parser.add_argument("--station", default="Lab-Station-1", help="Classroom station identifier")
    parser.add_argument("--simulate", action="store_true", help="Run without physical Arduino hardware")
    args = parser.parse_args()

    run_logger(args.port, args.baud, args.station, args.simulate)
