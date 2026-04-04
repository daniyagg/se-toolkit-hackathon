# toolkit_project
# Version 1 Plan – Water Tracker MVP

## Core Feature (one thing done well)
> **User can record one glass of water per click and see today’s progress (cups / goal).**

## Functional Scope

| Component | What it does |
|-----------|---------------|
| **Backend (FastAPI)** | Provides two REST endpoints: `GET /today/{user_id}` (returns current cups and fixed goal = 8) and `POST /drink/{user_id}` (increments cups for today). Returns JSON. |
| **Database (PostgreSQL)** | Single table `water_log` with columns: `id`, `user_id`, `date`, `cups`. Stores daily intake per user. |
| **Client (Flutter)** | Mobile app with a screen showing: today’s date, progress bar, text `X / 8 glasses`, and a button `+1 Glass`. On button tap, calls the API and updates UI dynamically. |

## What is NOT in Version 1
- User authentication (fixed `user_id` for demo, e.g. `"user_123"`)
- Setting custom goal (hardcoded to 8)
- History view (will be added in Version 2)
- Notifications / reminders
- Deployment (runs locally for demo)

## Success Criteria for Demo
- [ ] FastAPI server runs on `localhost:8000`
- [ ] PostgreSQL contains `water_log` table
- [ ] Flutter app launches on emulator/device
- [ ] Clicking `+1 Glass` increases the counter and progress bar
- [ ] Data persists after app restart (because stored in DB)
- [ ] TA can see API docs at `/docs` and raw DB content via `psql`
