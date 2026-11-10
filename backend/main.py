from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from backend.database import SessionLocal
from backend.models import SensorReading, BatteryReading
from sqlalchemy import delete, select
from contextlib import asynccontextmanager
import asyncio

async def cleanup_loop():
    while True:
        try:
            run_scheduled_cleanup()
        except Exception as error:
            print(f"Scheduled cleanup failed: {error}")

        await asyncio.sleep(24 * 60 * 60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(cleanup_loop())

    try:
        yield
    finally:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)

class SensorData(BaseModel):
    temperature: float
    timestamp: datetime

class SensorInput(BaseModel):
    temperature: float

class BatteryData(BaseModel):
    charge_percent: float
    is_charging: bool
    timestamp: datetime


class BatteryInput(BaseModel):
    charge_percent: float
    is_charging: bool

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Engineering Dashboard API is running"}

@app.get("/sensors", response_model=SensorData)
def get_sensors():
    db = SessionLocal()

    try:
        statement = (
            select(SensorReading)
            .order_by(SensorReading.timestamp.desc())
            .limit(1)
        )
        reading = db.scalars(statement).first()

        if reading is None:
            raise HTTPException(
                status_code=404,
                detail="No sensor readings have been saved yet",
            )

        return SensorData(
            temperature=reading.temperature,
            timestamp=reading.timestamp,
        )
    finally:
        db.close()

@app.get("/sensors/history", response_model=list[SensorData])
def get_sensor_history():
    db = SessionLocal()

    try:
        statement = (
            select(SensorReading)
            .order_by(SensorReading.timestamp.desc())
            .limit(100)
        )
        readings = db.scalars(statement).all()

        readings.reverse()

        return [
            SensorData(
                temperature=reading.temperature,
                timestamp=reading.timestamp,
            )
            for reading in readings
        ]
    finally:
        db.close()


        

def delete_expired_readings(db, cutoff):
    db.execute(
        delete(SensorReading).where(SensorReading.timestamp < cutoff)
    )
    db.execute(
        delete(BatteryReading).where(BatteryReading.timestamp < cutoff)
    )

def run_scheduled_cleanup():
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    db = SessionLocal()

    try:
        delete_expired_readings(db, cutoff)
        db.commit()
    finally:
        db.close()

@app.get("/battery", response_model=BatteryData)
def get_battery():
    db = SessionLocal()

    try:
        statement = (
            select(BatteryReading)
            .order_by(BatteryReading.timestamp.desc())
            .limit(1)
        )
        reading = db.scalars(statement).first()

        if reading is None:
            raise HTTPException(
                status_code=404,
                detail="No battery readings have been saved yet",
            )

        return BatteryData(
            charge_percent=reading.charge_percent,
            is_charging=reading.is_charging,
            timestamp=reading.timestamp,
        )
    finally:
        db.close()

@app.get("/battery/history", response_model=list[BatteryData])
def get_battery_history():
    db = SessionLocal()

    try:
        statement = (
            select(BatteryReading)
            .order_by(BatteryReading.timestamp.desc())
            .limit(240)
        )
        readings = db.scalars(statement).all()
        readings.reverse()

        return [
            BatteryData(
                charge_percent=reading.charge_percent,
                is_charging=reading.is_charging,
                timestamp=reading.timestamp,
            )
            for reading in readings
        ]
    finally:
        db.close()

@app.post("/battery", response_model=BatteryData)
def create_battery_reading(data: BatteryInput):
    timestamp = datetime.now(timezone.utc)
    cutoff = timestamp - timedelta(days=30)
    db = SessionLocal()

    try:
        reading = BatteryReading(
            charge_percent=data.charge_percent,
            is_charging=data.is_charging,
            timestamp=timestamp,
        )
        db.add(reading)
        delete_expired_readings(db, cutoff)
        db.commit()

        return BatteryData(
            charge_percent=reading.charge_percent,
            is_charging=reading.is_charging,
            timestamp=reading.timestamp,
        )
    finally:
        db.close()



@app.post("/sensors", response_model=SensorData)
def create_sensor_reading(data: SensorInput):
    timestamp = datetime.now(timezone.utc)
    cutoff = timestamp - timedelta(days=30)
    db = SessionLocal()


    try:
        reading = SensorReading(
            temperature=data.temperature,
            timestamp=timestamp,
        )
        db.add(reading)

        delete_expired_readings(db, cutoff)

        db.commit()

        return SensorData(
            temperature=reading.temperature,
            timestamp=reading.timestamp,
        )
    finally:
        db.close()