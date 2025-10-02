import os
import json
import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract(url):
    log_folder = "data/raw"
    os.makedirs(log_folder, exist_ok=True)

    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()  

        data = response.json()  
        logging.info("Fetched data and converted to JSON successfully")

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp_str}_response.json"
        full_path = os.path.join(log_folder, filename)

        with open(full_path, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Response saved to {full_path}")
        return data

    except requests.exceptions.Timeout:
        logging.error("Request timed out")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e} - Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
    except ValueError:
        logging.error("Failed to parse JSON")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")

    return None

