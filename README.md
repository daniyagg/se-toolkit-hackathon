# Version 1 Plan – WaterTracker MVP

## Core Feature (one thing done well)
> User can record one glass of water per click and see today's progress (cups / goal = 8).

## Architecture Overview
[Flutter Client] → [FastAPI Backend] → [PostgreSQL Database]


## Database (PostgreSQL)

**Table:** `water_log`

| Column   | Type      | Description                    |
|----------|-----------|--------------------------------|
| id       | SERIAL    | Primary key                    |
| user_id  | VARCHAR   | Telegram or fixed user ID      |
| date     | DATE      | YYYY-MM-DD                     |
| cups     | INTEGER   | Number of glasses (default 0)  |

**Constraints:** `UNIQUE(user_id, date)`

## Backend (FastAPI)

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/water/today/{user_id}`  | Returns `{cups, goal: 8}` for today |
| POST   | `/water/drink/{user_id}`  | Increments cups by 1, returns updated `{cups, goal: 8}` |

**Tech Stack:** FastAPI, SQLAlchemy, psycopg2-binary, Uvicorn

## Frontend (Flutter)

**Screen components:**
- Current date display
- Progress bar (cups / goal)
- Text: `X / 8 glasses`
- Button: `+1 Glass`

**Behaviour:**
- On load: fetch today's data via `GET /water/today/{user_id}`
- On button tap: send `POST /water/drink/{user_id}`, update UI with response

**Tech Stack:** Flutter, HTTP package

## What is NOT included in Version 1

- User authentication (hardcoded `user_id = "user_123"`)
- Custom goal setting (fixed to 8 glasses)
- History view (will be added in Version 2)
- Notifications / reminders

## Success Criteria for TA Demo

- [ ] FastAPI server runs on `http://localhost:8000`
- [ ] PostgreSQL contains `water_log` table with data
- [ ] Flutter app launches on emulator / real device
- [ ] Clicking `+1 Glass` increases counter and progress bar
- [ ] Data persists after app restart (stored in DB)
- [ ] TA can see API docs at `/docs` and raw DB via `psql`

## Time Estimate

| Task                     | Time    |
|--------------------------|---------|
| PostgreSQL setup + table | 15 min  |
| FastAPI endpoints        | 40 min  |
| Flutter UI + API calls   | 60 min  |
| Testing & polish         | 20 min  |
| **Total**                | **~2.5 hours** |
