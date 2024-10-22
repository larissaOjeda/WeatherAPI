from fastapi import FastAPI
from app.routers import weather

app = FastAPI()

app.include_router(weather.router)

# Command to run this project: uvicorn app.main:app --reload