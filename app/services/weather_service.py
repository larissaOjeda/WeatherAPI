import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
from datetime import datetime, timedelta

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)  # 1-hour cache
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

OPEN_METEO_URL = "https://climate-api.open-meteo.com/v1/climate"

def load_flight_data():
    file_path = "/Users/larissatrasvina/WeatherAPI/app/data/dataset.csv"
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')  


# Function to fetch weather data using Open-Meteo
async def fetch_weather(lat: float, lon: float, start_date: str, end_date: str):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max",
        "models": ["CMCC_CM2_VHR4", "FGOALS_f3_H", "HiRAM_SIT_HR", "MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR", "NICAM16_8S"]
    }

    responses = openmeteo.weather_api(OPEN_METEO_URL, params=params)

    response = responses[0]

    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": daily_temperature_2m_max
    }

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


async def get_weather_for_flights():
    mock_start_date = (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d")
    mock_end_date = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d")

    flights_data = load_flight_data()
    weather_report = []

    for ticket in flights_data:
        origin_lat = ticket['origin_latitude']
        origin_lon = ticket['origin_longitude']
        destination_lat = ticket['destination_latitude']
        destination_lon = ticket['destination_longitude']
        start_date = mock_start_date,  
        end_date = mock_end_date,   
        
        origin_weather = await fetch_weather(origin_lat, origin_lon, start_date, end_date)
        destination_weather = await fetch_weather(destination_lat, destination_lon, start_date, end_date)
        
        weather_model = {
            "flight":ticket["flight_num"], 
            "origin_airport":ticket["origin"],
            "origin_weather":f"{str(origin_weather['temperature_2m_max'].iloc[0])} °C", 
            "destination_airport":ticket["destination"],
            "destination_weather": f"{str(destination_weather['temperature_2m_max'].iloc[0])} °C", 
        }
        weather_report.append(weather_model)
    return weather_report
