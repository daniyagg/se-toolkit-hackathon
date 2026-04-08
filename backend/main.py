from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from databases import Database
from datetime import date, timedelta
from config import DATABASE_URL
from models import WaterResponse, DrinkResponse, HistoryResponse, HistoryEntry, UserLogin, UserRegister, UserResponse
import os
import hashlib

app = FastAPI(title="WaterTracker API", version="2.2.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database(DATABASE_URL)

# Serve web app
web_app_path = os.path.join(os.path.dirname(__file__), "..", "web_app")


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/", response_class=HTMLResponse)
async def serve_web_app():
    index_path = os.path.join(web_app_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return HTMLResponse("<h1>Web app not found. Run from project root.</h1>")


@app.on_event("startup")
async def startup():
    await database.connect()
    # Create users table if not exists
    await database.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/user/register", response_model=UserResponse)
async def user_register(user: UserRegister):
    """Register a new user with password"""
    username = user.username.strip()
    password = user.password
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    if len(password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")
    
    password_hash = hash_password(password)
    
    try:
        await database.execute(
            "INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)",
            values={"username": username, "password_hash": password_hash}
        )
        return UserResponse(user_id=username, message=f"Account created! Welcome, {username}!")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/user/login", response_model=UserResponse)
async def user_login(user: UserLogin):
    """Login with username and password"""
    username = user.username.strip()
    password = user.password
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    password_hash = hash_password(password)
    
    query = "SELECT username FROM users WHERE username = :username AND password_hash = :password_hash"
    row = await database.fetch_one(query, values={"username": username, "password_hash": password_hash})
    
    if not row:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return UserResponse(user_id=row["username"], message=f"Welcome back, {row['username']}!")


@app.get("/water/today/{user_id}", response_model=WaterResponse)
async def get_today_water(user_id: str):
    return await get_water_for_date(user_id, date.today())


@app.get("/water/date/{user_id}/{target_date}", response_model=WaterResponse)
async def get_water_for_date_endpoint(user_id: str, target_date: str):
    """Get water intake for a specific date (YYYY-MM-DD)"""
    try:
        target = date.fromisoformat(target_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    return await get_water_for_date(user_id, target)


async def get_water_for_date(user_id: str, target_date: date):
    query = """
        SELECT cups FROM water_log
        WHERE user_id = :user_id AND date = :date
    """
    row = await database.fetch_one(query, values={"user_id": user_id, "date": target_date})
    cups = row["cups"] if row else 0
    return WaterResponse(cups=cups, goal=8)


@app.post("/water/drink/{user_id}", response_model=DrinkResponse)
async def drink_water(user_id: str):
    return await update_water(user_id, date.today(), 1)


@app.post("/water/undo/{user_id}", response_model=DrinkResponse)
async def undo_water(user_id: str):
    """Reduce water intake by 1 glass"""
    today = date.today()
    
    # Check if there's data to undo
    query = """
        SELECT cups FROM water_log
        WHERE user_id = :user_id AND date = :date
    """
    row = await database.fetch_one(query, values={"user_id": user_id, "date": today})
    
    if not row or row["cups"] <= 0:
        raise HTTPException(status_code=400, detail="No water intake to undo")
    
    return await update_water(user_id, today, -1)


async def update_water(user_id: str, target_date: date, change: int):
    """Update water intake by change amount (positive or negative)"""
    query = """
        INSERT INTO water_log (user_id, date, cups)
        VALUES (:user_id, :date, :change)
        ON CONFLICT (user_id, date)
        DO UPDATE SET cups = GREATEST(water_log.cups + :change, 0)
        RETURNING cups, date
    """
    result = await database.fetch_one(query, values={
        "user_id": user_id, 
        "date": target_date,
        "change": change
    })
    
    return DrinkResponse(cups=result["cups"], goal=8, date=str(result["date"]))


@app.get("/water/history/{user_id}", response_model=HistoryResponse)
async def get_water_history(user_id: str):
    today = date.today()
    # Get the last 7 days
    history = []
    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        query = """
            SELECT cups FROM water_log
            WHERE user_id = :user_id AND date = :date
        """
        row = await database.fetch_one(query, values={"user_id": user_id, "date": target_date})
        cups = row["cups"] if row else 0
        history.append(HistoryEntry(date=str(target_date), cups=cups))
    
    return HistoryResponse(goal=8, history=history)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
