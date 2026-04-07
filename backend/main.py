from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from datetime import date
from config import DATABASE_URL
from models import WaterResponse, DrinkResponse

app = FastAPI(title="WaterTracker API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/water/today/{user_id}", response_model=WaterResponse)
async def get_today_water(user_id: str):
    today = date.today()
    query = """
        SELECT cups FROM water_log 
        WHERE user_id = :user_id AND date = :date
    """
    row = await database.fetch_one(query, values={"user_id": user_id, "date": today})
    
    cups = row["cups"] if row else 0
    return WaterResponse(cups=cups, goal=8)


@app.post("/water/drink/{user_id}", response_model=DrinkResponse)
async def drink_water(user_id: str):
    today = date.today()
    
    # Try to insert or update existing record
    query = """
        INSERT INTO water_log (user_id, date, cups) 
        VALUES (:user_id, :date, 1)
        ON CONFLICT (user_id, date) 
        DO UPDATE SET cups = water_log.cups + 1
        RETURNING cups, date
    """
    result = await database.fetch_one(query, values={"user_id": user_id, "date": today})
    
    return DrinkResponse(cups=result["cups"], goal=8, date=str(result["date"]))


@app.get("/health")
async def health_check():
    return {"status": "ok"}
