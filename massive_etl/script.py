import pandas as pd
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    filename="massive_etl/etl_errors.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Starting ETL process")

# first we are going to read the csv and clean the data by removing the rows that have less than 2 items

# we applied the 'generators' to read the csv in chunks of 100,000 rows to avoid memory errors
# note: the csv file below is heavy and not uploaded to github, but you can replace it with any massive csv
chunks = pd.read_csv("massive_etl/Library_Collection_Inventory.csv", chunksize=100000)

cleaned_chunks = []
for chunk in chunks:
    data = chunk[chunk["ItemCount"] > 1]

    cleaned_chunks.append(data)

for chunk_number, chunk in enumerate(cleaned_chunks):
    print(f"chunk {chunk_number}: {len(chunk)} rows")

# once we already have the cleaned chunks with the rows that we need we will link the sqlite database

connection = sqlite3.connect("massive_etl/library_test.db")
cursor = connection.cursor()

# and now we will create a table to store the data

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS library_collection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  BibNum INTEGER,
  Title TEXT,
  Author TEXT,
  ISBN TEXT,
  PublicationYear INTEGER,
  Publisher TEXT,
  Subjects TEXT,
  ItemType TEXT,
  ItemCollection TEXT,
  FloatingItem TEXT,
  ItemLocation TEXT,
  ReportDate TEXT,
  ItemCount INTEGER
)
"""
)

batch_size = 1000

try:
    for chunk in cleaned_chunks:
        # we convert the pandas dataframe to a simple list of lists to be able to insert it into sql
        data = chunk.values.tolist()

        # we slice the data into smaller batches of 1000 items each
        for x in range(0, len(data), batch_size):
            batch = data[x : x + batch_size]

            try:
                # we use executemany with parameterized queries (?,?) to do a bulk insert safely and prevent sql injection
                cursor.executemany(
                    f"""
                        INSERT INTO library_collection (BibNum,Title,Author,ISBN,PublicationYear,Publisher,Subjects,ItemType,ItemCollection,FloatingItem,ItemLocation,ReportDate,ItemCount) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    batch,
                )

            except Exception as error:
                # if a specific batch fails, we log the error but the script continues running
                logging.exception(
                    f"Error inserting batch starting at position {x}: {error}"
                )

    # if everything went well, we commit all the transactions to save them permanently
    connection.commit()
    logging.info("ETL process finished successfully")

except Exception as error:
    logging.exception(f"General ETL error: {error}")

finally:
    # no matter what happens (success or crash), we always make sure to close the database connection
    connection.close()
    logging.info("Database connection closed")
