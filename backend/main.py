from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Load database credentials from the .env file
load_dotenv()

app = FastAPI(title="Fitton Booth API")

# Configure CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to connect to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/")
def read_root():
    return {"status": "Fitton Booth Backend is running with PostgreSQL!"}

@app.get("/api/inventory")
def get_inventory():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # RealDictCursor formats the SQL rows directly into Python dictionaries (JSON)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, name, price, image_url, lens_id FROM dresses;")
        dresses = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"dresses": dresses}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))