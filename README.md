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



# Version 2 Plan – WaterTracker (Brief)

## Core improvements (choose based on TA feedback)

1. **History** – last 7 days as chart/list  
2. **Custom goal** – user sets own target (4–12 glasses)  
3. **Daily reminders** – local push notifications (10:00, 18:00)  
4. **Deployment** – backend on Render + cloud PostgreSQL, frontend APK  
5. **Polish** – loading indicators, error handling, pull-to-refresh

## Implementation steps

| Feature | What to do | Est. time |
|---------|-----------|-----------|
| History | `GET /history/{user_id}` + new screen in Flutter | 1h |
| Custom goal | Add `goal` column, `POST /goal`, settings UI | 1h |
| Reminders | `flutter_local_notifications`, schedule daily | 45m |
| Deployment | Render + Neon (cloud DB), build release APK | 1h |
| Polish | Loaders, error messages, pull-to-refresh | 30m |

## Deployment (minimal)

- **Backend:** `render.yaml` + PostgreSQL (Neon/Supabase)  
- **Frontend:** `flutter build apk --release` → share APK  

## Success criteria

- [ ] TA feedback from V1 addressed  
- [ ] App works with deployed backend (no local server needed)  
- [ ] New features work without crashes  
- [ ] TA can install APK on their phone and test  

## Total time

~4–5 hours
