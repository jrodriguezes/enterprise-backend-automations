import time
import requests
import tenacity
import logging

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# this is the worker. its job is get data, and deal with failures
# we use the retry pattern with exponential backoff if the external api is down
@tenacity.retry(
    stop=tenacity.stop_after_attempt(5), # try up to 5 times
    wait=tenacity.wait_exponential(multiplier=2, min=2, max=30), # wait 2s, 4s, 8s, etc.
    retry=tenacity.retry_if_exception_type(requests.exceptions.RequestException),
)
def fetch_frankfurter_api():
    logging.info("attempting to fetch data from frankfurter api...")
    # if this fails, tenacity will automatically catch the error and retry
    response = requests.get("https://api.frankfurter.dev/v2/rates?base=USD")
    
    # raise an error if the status code is not 200 (e.g. 503 or 429)
    response.raise_for_status() 
    
    return response.json()

def start_cron_job():
    while True:
        try:
            # the worker fetches the data
            rates_data = fetch_frankfurter_api()
            
            # the worker packages the data and posts it to the webhook
            logging.info("data fetched successfully. sending to webhook")
            webhook_response = requests.post("http://localhost:8000/update-rates", json=rates_data)
            
            logging.info(f"webhook responded with: {webhook_response.json()}")

        except Exception as error:
            # if we fail after all 5 retries, we log the critical error but keep the cron alive
            logging.error(f"worker failed to process job: {error}")

        # the cron goes to sleep for 15 minutes before repeating
        # for testing purposes, you can change this to 10 seconds
        logging.info("worker going to sleep for 15 minutes...")
        time.sleep(900) 

start_cron_job()
