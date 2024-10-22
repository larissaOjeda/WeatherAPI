from fastapi import APIRouter, HTTPException
from app.services.weather_service import get_weather_for_flights
from app.models.weather import WeatherResponseModel
from typing import List

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

@router.get("/flights-report", response_model=List[WeatherResponseModel])
async def get_weather_report():
    try:
        report = await get_weather_for_flights()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")
