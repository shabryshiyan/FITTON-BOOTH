from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

app = FastAPI(title="Fitton Booth API")

#Configure CORS to allow your Live Server frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Fitton Booth Backend is running!"}

@app.get("/api/inventory")
def get_inventory():
    # Placeholder: Later this will fetch real data from PostgreSQL
    return {
        "dresses": [
            {"id": 1, "name": "Red Summer Dress", "price": 45.99},
            {"id": 2, "name": "Blue Evening Gown", "price": 120.50}
        ]
    }