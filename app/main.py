# database\app\detabase\app\main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date, timedelta
import random

app = FastAPI(title="Manufacturing Index API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TimePoint(BaseModel):
    date: date
    value: float

class SeriesResponse(BaseModel):
    metric: str
    frequency: str
    series: List[TimePoint]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/timeseries", response_model=SeriesResponse)
def get_timeseries(metric: str = Query("mfg_index"), frequency: str = Query("weekly")):
    random.seed(42 if metric == "mfg_index" else 100)
    today = date.today()
    if frequency == "daily":
        points = 120
        step = 1
    else:
        points = 26
        step = 7
    start = today - timedelta(days=points*step)
    series = []
    level = 100.0 if metric == "mfg_index" else 1000.0
    for i in range(points):
        d = start + timedelta(days=i*step)
        val = level + (i * (0.15 if metric == "mfg_index" else 1.2)) + 3.0*(random.random()-0.5)
        if metric == "orders":
            val += 5.0*(random.random()-0.5) + 20.0*(i % 4 == 0)
        series.append({"date": d, "value": round(val, 2)})
    return {"metric": metric, "frequency": frequency, "series": series}

@app.get("/api/geo/activity")
def geo_activity():
    features = [
        {"type": "Feature", "properties": {"name": "Nagoya Plant A", "activity": 80}, "geometry": {"type": "Point", "coordinates": [136.9066, 35.1815]}},
        {"type": "Feature", "properties": {"name": "Yokohama Port", "activity": 65}, "geometry": {"type": "Point", "coordinates": [139.6380, 35.4437]}},
        {"type": "Feature", "properties": {"name": "Kobe Steel Area", "activity": 72}, "geometry": {"type": "Point", "coordinates": [135.1955, 34.6901]}},
        {"type": "Feature", "properties": {"name": "Kitakyushu Industrial Zone", "activity": 58}, "geometry": {"type": "Point", "coordinates": [130.8720, 33.8833]}},
    ]
    return {"type": "FeatureCollection", "features": features}
