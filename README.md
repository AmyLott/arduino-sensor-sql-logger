# Arduino Uno R4 Environmental Sensor & SQL Logger

An interdisciplinary STEM lab tool designed for high school Computer Science and Environmental Science courses. Students program physical sensors on an **Arduino Uno R4** using **Python**, stream real-time telemetry over USB serial, and persist validated records into a **SQLite relational database** for statistical analysis.

## Features
- **Hardware-to-Database Pipeline:** Streams live temperature and humidity data from an Arduino Uno R4 to a host Python ingestion script.
- **Data Validation & Integrity:** Filters malformed serial packets and out-of-range sensor spikes before database insertion.
- **Built-in Simulation Mode:** Includes a `--simulate` flag so students and reviewers can test the SQL schema and queries without physical hardware attached.
- **SQL Aggregate Reporting:** Automatically computes session averages, minimums, and maximums upon exit.

## Tech Stack
- **Embedded Hardware:** Arduino Uno R4 (MicroPython)
- **Backend & Data Ingestion:** Python 3, `pyserial`, `sqlite3`
- **Database:** SQLite

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AmyLott/arduino-sensor-sql-logger.git](https://github.com/AmyLott/arduino-sensor-sql-logger.git)
   cd arduino-sensor-sql-logger
