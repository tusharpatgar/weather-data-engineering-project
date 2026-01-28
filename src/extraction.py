import requests
import json 
from datetime import datetime,timezone
import os
from pathlib import Path

BASE_URL="https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 12.07,
	"longitude": 77.50,
	"hourly": [
        "temperature_2m", 
        "relative_humidity_2m",
         "dew_point_2m", 
         "apparent_temperature", 
         "precipitation_probability", 
         "precipitation", 
         "rain", 
         "showers"],
    "timezone": "auto"
}

SOURCE=Path(__file__).parent
PROJECTDIR=SOURCE.parent
RAW_DIR=PROJECTDIR /"data"/"raw"
source="open-meteo"

def build_params(params):
    query_params=params.copy()
    if isinstance(query_params.get("hourly"),list):
        query_params["hourly"]=",".join(query_params["hourly"])
    return query_params

def fetch_weather_api():
    query_params=build_params(params)
    response=requests.get(BASE_URL,params=query_params,timeout=10)
    response.raise_for_status()

    return response.json()

def save_data(data):
    os.makedirs(RAW_DIR,exist_ok=True)

    timestamp=datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename=f"weather_{source}_{timestamp}.json"
    file_path=os.path.join(RAW_DIR,filename)

    with open(file_path,"w") as f:
        json.dump(data,f,indent=2)
    
    return file_path



def main():
    try:
        data=fetch_weather_api()
        save_data(data)
    except requests.exceptions.RequestException as e:
        print(f"Api fetching failed :{e}")
    except Exception as e:
        print("Unexpected Error:{e}")

if __name__=="__main__":
    main()