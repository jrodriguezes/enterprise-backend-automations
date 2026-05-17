# Resilient API Sychronizer & Webhook

This microservice architecture demonstrates how to securely consume unstable external APIs and safely store the data using an event-driven approach. 

The project is split into two decoupled components to prevent HTTP timeouts and ensure data integrity.

## Architecture

1. **Background Worker (`worker_cron.py`)**: 
   Acts as the data gatherer. It reaches out to external providers (in this case, the Frankfurter Exchange Rate API) to fetch data. Because external networks are unreliable, it implements a **Retry Pattern with Exponential Backoff** (using `tenacity`). It will wait and retry gracefully before reporting a failure. Once the data is secured, it sends it via a POST request.

2. **Passive Webhook (`webhook_api.py`)**: 
   A high-performance FastAPI endpoint that acts purely as a receiver. It does not make outbound network requests. When it receives the JSON payload from the worker, it immediately processes it and performs a bulk insert into a local SQLite database, returning a success status in milliseconds.

## Key Technical Concepts

- **Fault Tolerance:** Exponential backoff ensures the system doesn't crash during temporary network outages and avoids spamming the provider with DDoS-like immediate retries.
- **Inversion of Control:** By decoupling the fetching logic from the webhook, we eliminate the risk of HTTP Timeout errors that occur when APIs take too long to respond.
- **Bulk Database Operations:** Reuses the concept of `executemany` to insert all API records in a single database transaction, ensuring ACID compliance.

## Tech Stack

- **Python 3.11**
- **FastAPI / Uvicorn** (High-performance async web framework)
- **Requests** (HTTP client)
- **Tenacity** (Retry and backoff library)
- **SQLite3** (Local storage)

## How to run

1. Start the webhook server:
   ```bash
   uvicorn webhook_api:app --reload
   ```
2. In a separate terminal, start the background worker:
   ```bash
   python worker_cron.py
   ```
