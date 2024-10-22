from pydantic import BaseModel
from typing import Optional, List

class WeatherResponseModel(BaseModel):
    flight: Optional[int]
    origin_airport:  Optional[str]
    origin_weather: Optional[str]
    destination_airport: Optional[str]
    destination_weather: Optional[str]
