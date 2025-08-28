# In backend/app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import attacks

app = FastAPI()

# Add CORS middleware to allow the frontend to access the API
origins = [
    "http://127.0.0.1:5500",  # Your frontend's local development server
    "http://localhost:8000"   # Your backend's own address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attacks.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the DDoS Attack Map API"}