from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Engineering Dashboard API is running"}

@app.get("/sensors")
def get_sensors():
    temperature = round(random.uniform(20, 60), 1)
    voltage = round(random.uniform(11.5, 13.0), 2)
    current = round(random.uniform(1, 5), 2)

    return {
        "temperature": temperature,
        "voltage": voltage,
        "current": current
    }