# Automated Reporting & SMTP Alerts

This module generates automated daily reports from an existing database and distributes them via an SMTP email notification system.

## Architecture

1. **Excel Generator (`daily_excel_report.py`)**: 
   Connects to the SQLite database to query datasets, transforms the raw SQL tuples into a structured Pandas DataFrame, and exports the data directly into a structured `.xlsx` file.

2. **Alert Notifier (`alert_notifier.py`)**: 
   Constructs a secure `EmailMessage` with binary attachments, specifies the correct MIME types to bypass modern spam filters, and uses an SSL-encrypted `smtplib` connection to dispatch the report.

## Key Technical Concepts

- **Pandas to Excel:** Direct conversion from SQL cursors to `.xlsx` bypassing manual loops.
- **Secure Attachments:** Reading files in `rb` (read binary) mode and utilizing `pathlib` for dynamic filename extraction.
- **SMTP & SSL:** Utilizing `SMTP_SSL` to securely authenticate and dispatch emails programmatically.

## Tech Stack

- **Python 3.11**
- **Pandas / OpenPyXL** (Data structuring and Excel engine)
- **SQLite3** (Database connection)
- **Smtplib / Email** (Native Python networking and SSL libraries)
