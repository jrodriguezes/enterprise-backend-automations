import pandas as pd
import sqlite3
from alert_notifier import send_email_with_attachment

# connect to the database from the previous resilient webhook practice
connection = sqlite3.connect("./api_webhook_resilience/usd-rates.db")
cursor = connection.cursor()

# extract all records (this could easily be filtered by date using a where clause)
cursor.execute("SELECT * FROM usd_rates")
rates = cursor.fetchall()

# load the sql output directly into a pandas dataframe for fast tabular manipulation
df = pd.DataFrame(rates, columns=["id", "date", "base", "quote","rate"])

# define the path where our daily report will be saved
excel_path = "automated_reporting_alerts/daily_rate_report.xlsx"

# convert the dataframe into an excel file without the row index numbers
df.to_excel(excel_path, index=False)

# trigger the alert notifier to send the file via email
send_email_with_attachment(excel_path)

print("excel generated and email sent successfully")