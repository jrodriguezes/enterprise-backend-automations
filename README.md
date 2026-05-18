# Enterprise Backend Automations & Pipelines

Welcome to my technical portfolio. This repository contains a collection of backend microservices, data processing scripts, and automation workflows designed to solve enterprise-level challenges in logistics, data ingestion, and system resilience.

## Projects Overview

### 1. [Massive CSV ETL Pipeline](./massive_etl/)
A memory-efficient Python pipeline built to process massive datasets (e.g., Inventory, Logistics logs) that exceed system RAM. 
*   **Key skills:** Chunked processing, Bulk SQL insertions (`executemany`), Memory Management (`pandas`), Error Logging.

### 2. [Resilient API Webhook & Cron Worker](./api_webhook_resilience/)
An event-driven microservices architecture decoupling API consumption from database ingestion to prevent HTTP timeouts.
*   **Key skills:** External API integrations, Retry Patterns & Exponential Backoff (`tenacity`), Event Receivers / Webhooks (`FastAPI`), ACID SQL Transactions.

*(More automation practices coming soon...)*

## Technology Stack
*   **Language:** Python 3.11+
*   **Frameworks:** FastAPI, Uvicorn
*   **Data Processing:** Pandas
*   **Database:** SQLite3 (parameterized queries for SQL Injection prevention)
*   **Resilience:** Tenacity, Requests

## Engineering Philosophy
All projects in this repository focus on:
1. **Performance:** Not relying on ORMs when raw SQL is faster for bulk operations.
2. **Resilience:** Expecting and gracefully handling external failures.
3. **Security:** Implementing parameterized queries and hiding sensitive keys.