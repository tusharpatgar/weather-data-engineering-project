import json
import logging
from datetime import datetime
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

SOURCE = "open-meteo"

def transform_data(raw_data):
    logging.info("Starting Transformation")

    latitude = raw_data.get("latitude")
    longitude = raw_data.get("longitude")
    city = "Bangalore"
    hourly_data = raw_data.get("hourly", {})
    
    timestamps = hourly_data.get("time", [])
    temperature = hourly_data.get("temperature_2m", [])
    relative_humidity = hourly_data.get("relative_humidity_2m", [])
    dew_point_2m = hourly_data.get("dew_point_2m", [])
    apparent_temperature = hourly_data.get("apparent_temperature", [])
    precipitation_probability = hourly_data.get("precipitation_probability", [])
    precipitation = hourly_data.get("precipitation", [])
    rain = hourly_data.get("rain", [])
    showers = hourly_data.get("showers", [])

    records = []

    for idx, obs_time in enumerate(timestamps):
        try:
            record = {
                "source": SOURCE,
                "city": city,
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": obs_time,
                "temperature_2m": temperature[idx],
                "relative_humidity_2m": relative_humidity[idx],
                "dew_point_2m": dew_point_2m[idx], 
                "apparent_temperature": apparent_temperature[idx], 
                "precipitation_probability": precipitation_probability[idx],
                "precipitation": precipitation[idx],
                "rain": rain[idx] ,
                "showers": showers[idx]
            }
            records.append(record)
        except Exception as e:
            logging.error(f"Error processing timestamp {obs_time}: {e}")

    logging.info(f"Transformation complete: {len(records)} records created")
    print(records)

