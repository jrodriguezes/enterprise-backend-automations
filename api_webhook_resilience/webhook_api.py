from fastapi import FastAPI, Request
import sqlite3
import logging

# configure logging just like in the previous practice
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# this is the webhook. its only job is to stay awake and receive data
@app.post("/update-rates")
async def receive_webhook(request: Request):
    # we receive the json payload that the worker sent us
    data = await request.json()
    
    # we connect to the database 
    connection = sqlite3.connect("usd-rates.db")
    cursor = connection.cursor()

    try:
        # we ensure the table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usd_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATETIME NOT NULL,
                base VARCHAR NOT NULL,
                quote VARCHAR NOT NULL,
                rate FLOAT NOT NULL
            )
            """
        )

        # we prepare the data for a bulk insert just like in the etl practice
        values = []
        for x in data:
            values.append((x["base"], x["date"], x["quote"], x["rate"]))

        # we use executemany to securely insert all the records at once
        cursor.executemany(
            """
            INSERT INTO usd_rates (base, date, quote, rate) VALUES (?, ?, ?, ?)
            """,
            values,
        )

        connection.commit()
        logging.info(f"successfully saved {len(values)} rates to the database")

    except Exception as error:
        logging.exception(f"database error: {error}")
        return {"status": "error", "message": str(error)}

    finally:
        # always close the database connection
        connection.close()

    # the webhook responds immediately (no timeouts)
    return {"status": "success"}
