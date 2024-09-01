import requests
import sched
import time
import logging
import threading
import os
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Read configuration from environment variables
BOOKSTACK_URL = os.getenv('BOOKSTACK_URL', 'https://wiki.rlvd.duckdns.org')
AUTH_TOKEN = os.getenv('AUTH_TOKEN', '')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', '300'))  # default to 300 seconds

# Define a global variable to store results and a lock for thread safety
results = {}
results_lock = threading.Lock()

# Function to fetch data from a specific API endpoint
def fetch_api_data(endpoint):
    try:
        headers = {'Authorization': f'Token {AUTH_TOKEN}'} if AUTH_TOKEN else {}
        response = requests.get(f"{BOOKSTACK_URL}/api/{endpoint}", headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
        logging.info(f"Fetched data from {endpoint}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {endpoint}: {e}")
        return None

# Function to update data periodically
def update_data(sc):
    global results
    logging.info("Updating data...")

    try:
        # Fetch data from the hardcoded endpoints
        books_data = fetch_api_data('books')
        pages_data = fetch_api_data('pages')

        if books_data is None or pages_data is None:
            raise Exception("Failed to fetch data from one or more endpoints")

        updated_results = {
            'total_books': books_data.get('total', 0),
            'total_pages': pages_data.get('total', 0)
        }

        with results_lock:
            results = updated_results  # Update the global 'results' variable
            logging.info("Data updated successfully.")
    except Exception as e:
        logging.error(f"Error during update: {e}")

    # Schedule the next update
    sc.enter(UPDATE_INTERVAL, 1, update_data, (sc,))
    logging.info(f"Scheduled next update in {UPDATE_INTERVAL} seconds.")

# Initialize Flask app
app = Flask(__name__)

# Endpoint to serve results
@app.route('/', methods=['GET'])
def get_results():
    logging.info("Received GET request for /")
    with results_lock:
        return jsonify(results)

# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        scheduler.run(blocking=False)
        time.sleep(1)  # sleep to prevent high CPU usage

if __name__ == '__main__':
    # Start the scheduler thread
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, update_data, (scheduler,))
    logging.info("Scheduled first update immediately.")
    
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logging.info("Started the scheduler thread.")

    # Start Flask app with custom settings to avoid development server warnings
    app.run(host='0.0.0.0', port=4001, debug=False, use_reloader=False)

