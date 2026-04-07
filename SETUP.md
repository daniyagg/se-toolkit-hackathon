# WaterTracker

A water intake tracking application built with Flutter, FastAPI, and PostgreSQL.

## Features

- **Track Daily Water Intake**: Record glasses of water with a single tap
- **Progress Visualization**: See your daily progress towards the 8-glass goal
- **7-Day History**: View your water intake history for the last 7 days
- **Persistent Storage**: All data is stored in PostgreSQL

## Architecture

```
[Flutter Client] → [FastAPI Backend] → [PostgreSQL Database]
```

## Prerequisites

- **Flutter SDK** (3.0.0 or higher)
- **Python** (3.10 or higher)
- **PostgreSQL** (12 or higher)

## Setup Instructions

### 1. PostgreSQL Database Setup

```bash
# Connect to PostgreSQL
psql -U postgres

# Run the schema script
\i backend/schema.sql

# Or manually:
CREATE DATABASE watertracker;
\c watertracker
CREATE TABLE IF NOT EXISTS water_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    cups INTEGER NOT NULL DEFAULT 0,
    UNIQUE(user_id, date)
);
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Update database connection in config.py if needed
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/watertracker"

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 3. Flutter App Setup

```bash
# Navigate to flutter directory
cd flutter_app

# Get dependencies
flutter pub get

# Run the app
flutter run
```

> **Note**: Update the `baseUrl` in `lib/services/api_service.dart` if your backend is running on a different host/port.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/water/today/{user_id}` | Returns today's water intake |
| POST | `/water/drink/{user_id}` | Record a glass of water |
| GET | `/water/history/{user_id}` | Get 7-day water intake history |

## Database Schema

**Table:** `water_log`

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | VARCHAR(255) | User identifier |
| date | DATE | Date of entry (YYYY-MM-DD) |
| cups | INTEGER | Number of glasses (default: 0) |

**Constraints:** `UNIQUE(user_id, date)`

## Project Structure

```
se-toolkit-hackathon/
├── README.md
├── backend/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Pydantic models
│   ├── config.py         # Database configuration
│   ├── requirements.txt  # Python dependencies
│   └── schema.sql        # Database schema
└── flutter_app/
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── services/
        │   └── api_service.dart
        └── screens/
            └── home_screen.dart
```

## Development

### Running Tests

```bash
# Backend (add pytest to requirements.txt first)
cd backend
pytest

# Flutter
cd flutter_app
flutter test
```

### API Documentation

Once the backend is running, visit `http://localhost:8000/docs` to see the interactive API documentation provided by FastAPI/Swagger.

## License

MIT
