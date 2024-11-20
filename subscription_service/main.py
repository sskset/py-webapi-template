from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Subscription Service"}
