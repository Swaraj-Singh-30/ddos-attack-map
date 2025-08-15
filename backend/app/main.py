from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from .api.endpoints import attacks

app = FastAPI()

app.include_router(attacks.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the DDoS Attack Map API"}