# Massive Data ETL (Python)

This project is a practical implementation of an ETL. It is designed to handle massive datasets (e.g., an 850MB CSV file with millions of rows) without exhausting the system's RAM, ensuring data integrity and fast database insertions.

## Key Features & Technical Concepts

- **Memory Optimization (Batch Processing):** Uses `pandas` with `chunksize` to read the massive CSV file in chunks of 100,000 rows. This prevents "Out of Memory" errors that typically occur when loading large datasets.
- **Data Transformation (Cleaning):** Filters out irrelevant data on the fly (e.g., removing records where `ItemCount <= 1`) before loading it into the database.
- **High-Performance Database Loading (Bulk Inserts):** Instead of executing row-by-row `INSERT` statements, the script chunks the data into batches of 1,000 and uses `sqlite3`'s `executemany()`. This drastically reduces I/O operations and database locking.
- **Security:** Uses parameterized queries `(?, ?, ...)` to prevent SQL Injection attacks.
- **Resilience & Observability:** Implements robust `try/except` blocks to isolate errors at the batch level (so one bad row doesn't crash the entire 850MB process). All events and errors are recorded using Python's native `logging` module to a local `etl_errors.log` file.

## Tech Stack

- **Python 3.11**
- **Pandas** (Data extraction and transformation)
- **SQLite3** (Native database for local storage)
- **Logging** (Standard library for system observability)

## How it Works

1. **Extract:** The script connects to `Library_Collection_Inventory.csv` and reads it in fragments.
2. **Transform:** It converts the Pandas DataFrames into native Python lists and removes unneeded records.
3. **Load:** It creates a table (`library_collection`) if it doesn't exist, and pushes the data in batches of 1,000 records to `library_test.db`.
4. **Close:** Ensures the database connection is securely closed using a `finally` block, regardless of success or failure.

## Note on Data

The dataset used for this practice is a massive Library Collection Inventory CSV file. However, the exact same logic applies to processing logistics tracking logs, financial transactions, or user telemetry data.