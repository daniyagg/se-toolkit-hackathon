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

**Tech Stack:** FastAPI, PostgreSQL

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

## Success Criteria for Demo

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



# Water Tracker v2 – 7-Day History Feature Plan

## Feature
- Today's progress: `X / 8 glasses` with **+1 Glass** button
- Intake history for the last 7 days

## API (FastAPI)

| Method | Endpoint                   | Description |
|--------|----------------------------|-------------|
| GET    | `/water/today/{user_id}`   | `{cups, goal:8}` for today |
| POST   | `/water/drink/{user_id}`   | Increment `cups` by 1, return updated today |
| GET    | `/water/history/{user_id}` | `{goal:8, history: [{date, cups}]}` for last 7 days (missing days = 0) |

## Flutter UI
- Date header
- Progress bar + `X / 8`
- **+1 Glass** button
- Horizontal week chart (abbreviated weekdays + cups)

## Success Criteria
- [ ] App runs, fetches from `localhost:8000`
- [ ] Tap **+1** updates today
- [ ] History shows 7-day values (zeros for gaps)
- [ ] Data persists after restart
- [ ] `/docs` shows `/history` endpoint

## Time Estimate
| Task                         | Time   |
|------------------------------|--------|
| History SQL query            | 10 min |
| `/history` endpoint          | 25 min |
| Flutter history UI           | 50 min |
| Flutter API integration      | 30 min |
| Testing & polish             | 20 min |
| **Total**                    | **~2h 15m** |
