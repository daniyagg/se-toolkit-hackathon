# WaterTracker

A water intake tracking application. Two versions available:

- **v1** — Simple tracker with a single `+1 Glass` button
- **v2** — Full tracker with authentication, history, `-1 Glass`, and date navigation

---

## Version 1: Basic Tracker

A simple water intake tracker with a single button to log your daily water consumption.

### Features

- **Track Daily Water Intake**: Record glasses of water with a single click
- **Progress Visualization**: See your daily progress towards the 8-glass goal
- **Persistent Storage**: All data is stored in PostgreSQL

### Architecture

```
[Web Client (FastAPI)] → [FastAPI Backend] → [PostgreSQL Database]
```

### Quick Start

```bash
# Start the backend (includes web interface)
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web application interface |
| GET | `/water/today/{user_id}` | Returns today's water intake |
| POST | `/water/drink/{user_id}` | Record a glass of water (+1) |
| GET | `/health` | Health check endpoint |
| GET | `/docs` | Interactive API documentation |

### Database (PostgreSQL)

**Table:** `water_log`

| Column   | Type      | Description                    |
|----------|-----------|--------------------------------|
| id       | SERIAL    | Primary key                    |
| user_id  | VARCHAR   | User identifier                |
| date     | DATE      | YYYY-MM-DD                     |
| cups     | INTEGER   | Number of glasses (default 0)  |

**Constraints:** `UNIQUE(user_id, date)`

### Backend (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/water/today/{user_id}` | Returns `{cups, goal: 8}` for today |
| POST | `/water/drink/{user_id}` | Increments cups by 1, returns `{cups, goal: 8, date}` |

**Tech Stack:** FastAPI, PostgreSQL

### Frontend (Web App)

**Tracker Screen:**
- Progress bar (cups / goal)
- `+1 Glass 💧` button (centered)

**Behaviour:**
- On `+1 Glass` tap: send `POST /water/drink/{user_id}`, update UI

**Tech Stack:** Vanilla HTML/CSS/JavaScript, Fetch API

### Success Criteria for Demo

- [ ] FastAPI server runs on `http://localhost:8000`
- [ ] PostgreSQL contains `water_log` table with data
- [ ] Clicking `+1 Glass` increases counter and progress bar
- [ ] Data persists after app restart (stored in DB)
- [ ] TA can see API docs at `/docs` and raw DB via `psql`

### Time Estimate

| Task                         | Time    |
|------------------------------|---------|
| PostgreSQL setup + tables    | 20 min  |
| FastAPI water endpoints      | 30 min  |
| Web UI + API integration     | 40 min  |
| Testing & polish             | 10 min  |
| **Total**                    | **~1.5 hours** |

---

## Version 2: Full Tracker

A water intake tracking application with user authentication, 7-day history visualization, and date navigation.

### Features

- **User Authentication**: Secure registration and login with password protection
- **Track Daily Water Intake**: Record glasses of water with a single click
- **Undo Mistakes**: `-1 Glass` button to remove accidentally logged glasses
- **Progress Visualization**: See your daily progress towards the 8-glass goal
- **7-Day History**: View your water intake history for the last 7 days with bar chart
- **Date Navigation**: Browse between days with left/right arrows
- **Auto-Reset at Midnight**: Automatically switches to today's date at 0:00
- **Persistent Storage**: All data is stored in PostgreSQL
- **Web Interface**: No Flutter SDK required - works directly in your browser

### Architecture

```
[Web Client (FastAPI)] → [FastAPI Backend] → [PostgreSQL Database]
```

### Quick Start

```bash
# Start the backend (includes web interface)
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web application interface |
| POST | `/user/register` | Register a new user with password |
| POST | `/user/login` | Login with username and password |
| GET | `/water/today/{user_id}` | Returns today's water intake |
| GET | `/water/date/{user_id}/{target_date}` | Get water intake for specific date (YYYY-MM-DD) |
| POST | `/water/drink/{user_id}` | Record a glass of water (+1) |
| POST | `/water/undo/{user_id}` | Remove a glass of water (-1) |
| GET | `/water/history/{user_id}` | Get 7-day water intake history |
| GET | `/health` | Health check endpoint |
| GET | `/docs` | Interactive API documentation |

### Database (PostgreSQL)

**Table:** `water_log`

| Column   | Type      | Description                    |
|----------|-----------|--------------------------------|
| id       | SERIAL    | Primary key                    |
| user_id  | VARCHAR   | User identifier                |
| date     | DATE      | YYYY-MM-DD                     |
| cups     | INTEGER   | Number of glasses (default 0)  |

**Constraints:** `UNIQUE(user_id, date)`

**Table:** `users`

| Column        | Type         | Description                    |
|---------------|--------------|--------------------------------|
| id            | SERIAL       | Primary key                    |
| username      | VARCHAR(255) | Unique username                |
| password_hash | VARCHAR(255) | SHA-256 hashed password        |
| created_at    | TIMESTAMP    | Account creation timestamp     |

**Constraints:** `UNIQUE(username)`

### Backend (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/register` | Create account with `{username, password}`, returns `{user_id, message}` |
| POST | `/user/login` | Authenticate with `{username, password}`, returns `{user_id, message}` |
| GET | `/water/today/{user_id}` | Returns `{cups, goal: 8}` for today |
| GET | `/water/date/{user_id}/{target_date}` | Returns `{cups, goal: 8}` for specific date |
| POST | `/water/drink/{user_id}` | Increments cups by 1, returns `{cups, goal: 8, date}` |
| POST | `/water/undo/{user_id}` | Decrements cups by 1 (min 0), returns `{cups, goal: 8, date}` |
| GET | `/water/history/{user_id}` | Returns `{goal: 8, history: [{date, cups}]}` for last 7 days |

**Tech Stack:** FastAPI, PostgreSQL, SHA-256 password hashing

### Frontend (Web App)

**Authentication Screen:**
- Login/Register tabs
- Username + password input fields
- Password confirmation for registration
- Session persistence via localStorage

**Tracker Screen:**
- User header with logout button
- Date navigation (◀ ▶) with "TODAY" badge
- Progress bar (cups / goal)
- `+1 Glass 💧` button (centered)
- `-1 Glass ↩` button (centered, only for today)
- 7-day history bar chart (centered below buttons)

**Behaviour:**
- On load: check for saved session, auto-login if exists
- On login: authenticate via `POST /user/login`, save session
- On register: create account via `POST /user/register`, save session
- On date navigation: fetch data via `GET /water/date/{user_id}/{target_date}`
- On `+1 Glass` tap: send `POST /water/drink/{user_id}`, update UI
- On `-1 Glass` tap: send `POST /water/undo/{user_id}`, update UI
- At midnight (0:00): auto-switch to today's date with notification

**Tech Stack:** Vanilla HTML/CSS/JavaScript, Fetch API

### Success Criteria for Demo

- [ ] FastAPI server runs on `http://localhost:8000`
- [ ] PostgreSQL contains `water_log` and `users` tables with data
- [ ] User can register with username + password
- [ ] User can login with correct credentials
- [ ] Login fails with incorrect password
- [ ] Clicking `+1 Glass` increases counter and progress bar
- [ ] Clicking `-1 Glass` decreases counter (minimum 0)
- [ ] Date navigation works (browse past/future days)
- [ ] History shows 7-day values with bar chart (zeros for gaps)
- [ ] Auto-switch to today at midnight (0:00)
- [ ] Data persists after app restart (stored in DB)
- [ ] TA can see API docs at `/docs` and raw DB via `psql`

### Time Estimate

| Task                         | Time    |
|------------------------------|---------|
| PostgreSQL setup + tables    | 20 min  |
| User auth endpoints          | 30 min  |
| FastAPI water endpoints      | 40 min  |
| Web UI + API integration     | 60 min  |
| Date navigation + midnight   | 30 min  |
| Testing & polish             | 20 min  |
| **Total**                    | **~3.5 hours** |
