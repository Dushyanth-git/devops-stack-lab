from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from contextlib import asynccontextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data.xlsx")


class Record(BaseModel):
    name: str
    score: int

def ensure_file():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        df = pd.DataFrame(columns=["name", "score"])
        df.to_excel(FILE, index=False, engine="openpyxl")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_file()
    yield

app = FastAPI(lifespan=lifespan)   # ✅ app defined here

@app.get("/records")
def get_records():
    df = pd.read_excel(FILE)
    df = pd.read_excel(FILE, engine="openpyxl")
    return df.to_dict(orient="records")

@app.post("/records")
def add_records(record: Record):
    df = pd.read_excel(FILE, engine="openpyxl")
    df = pd.concat([df, pd.DataFrame([record.model_dump()])], ignore_index=True)
    df.to_excel(FILE, index=False, engine="openpyxl")

    return {"message": "Record added"}
