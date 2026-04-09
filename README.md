# WaterTracker

A daily water intake tracking web application with user authentication, 7-day history visualization, and date navigation.

---

## Demo

### Authentication

Users register or log in with a username and password. Sessions are persisted so returning users are automatically signed in.

### Tracker

After logging in, users see their daily progress toward an 8-glass goal. A single tap on **+1 Glass** logs a glass of water; **-1 Glass** removes an accidentally logged glass. Date navigation arrows let users browse past or future days, and a 7-day bar chart shows recent history at a glance.

>
![Login and Register screen](/screenshots/auth.png)
![Tracker screen with progress bar and history chart](/screenshots/tracker.png)

---

## Product Context

### End Users

Anyone who wants to stay hydrated — students, office workers, athletes, or health-conscious individuals who struggle to drink enough water throughout the day.

### Problem

Many people forget to drink water regularly and have no simple way to track their daily intake. Existing apps are often bloated with features, require accounts on proprietary platforms, or are mobile-only.

### Solution

WaterTracker is a lightweight, open-source web app that lets users log glasses of water with a single click, visualize their progress, and review the last 7 days — all from any browser. No app install required.

---

## Features

### Implemented

| Feature | Status |
|---------|--------|
| User registration & login (SHA-256 password hashing) | ✅ |
| Session persistence (auto-login) | ✅ |
| Log a glass of water (+1) | ✅ |
| Undo a logged glass (-1, today only) | ✅ |
| Daily progress bar (goal: 8 glasses) | ✅ |
| Date navigation (browse any day) | ✅ |
| 7-day history bar chart | ✅ |
| Auto-reset to today at midnight | ✅ |
| PostgreSQL persistent storage | ✅ |
| Interactive API docs (Swagger) | ✅ |
| Responsive web UI (vanilla HTML/CSS/JS) | ✅ |

### Not Yet Implemented

| Feature | Priority |
|---------|----------|
| Custom daily goal per user | Low |
| Email / push reminders to drink | Medium |
| Export data (CSV / PDF) | Low |
| Mobile app (Flutter) | Medium |
| OAuth / social login | Low |
| Multi-language support (i18n) | Low |
| Docker Compose one-command deploy | Medium |

---

## Usage

### Web App (Recommended)

1. Start the backend server (see **Deployment** below).
2. Open a browser and navigate to `http://localhost:8000`.
3. Register a new account or log in.
4. Tap **+1 Glass** each time you drink a glass of water.
5. Use the date arrows to review past days; the bar chart shows the last 7 days.

### API

The REST API can be explored interactively at `http://localhost:8000/docs` once the server is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/user/register` | Register — `{username, password}` → `{user_id, message}` |
| `POST` | `/user/login` | Login — `{username, password}` → `{user_id, message}` |
| `GET` | `/water/today/{user_id}` | Today's intake — `{cups, goal}` |
| `GET` | `/water/date/{user_id}/{date}` | Intake for a specific date |
| `POST` | `/water/drink/{user_id}` | Log +1 glass |
| `POST` | `/water/undo/{user_id}` | Undo -1 glass |
| `GET` | `/water/history/{user_id}` | 7-day history |
| `GET` | `/health` | Health check |

---

## Deployment

### Target OS

Ubuntu 24.04 LTS (same as university VMs).

### Prerequisites

The following must be installed on the VM:

| Software | Minimum Version | Install Command |
|----------|-----------------|-----------------|
| Python | 3.10+ | `sudo apt install python3 python3-venv python3-pip` |
| PostgreSQL | 14+ | `sudo apt install postgresql postgresql-contrib` |
| Nginx *(optional, for production)* | any | `sudo apt install nginx` |

### Step-by-Step Instructions

#### 1. Install PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

#### 2. Create the Database

```bash
sudo -u postgres psql <<EOF
CREATE DATABASE watertracker;
EOF
```

#### 3. Clone the Repository

```bash
git clone https://github.com/<your-username>/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

#### 4. Set Up the Python Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Configure the Database Connection

Edit `backend/config.py` if the default connection string does not match your setup:

```python
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/watertracker"
```

#### 6. Start the Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

The app (and its interactive API docs) will be available at:

- **App:** `http://<vm-ip>:8000`
- **API Docs:** `http://<vm-ip>:8000/docs`

#### 7. (Optional) Run Behind Nginx for Production

```bash
sudo cp web_app/nginx.conf /etc/nginx/sites-available/watertracker
sudo ln -s /etc/nginx/sites-available/watertracker /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Update `web_app/nginx.conf` to point `proxy_pass` to `http://127.0.0.1:8000`.

#### 8. (Optional) Run as a Systemd Service

```bash
sudo tee /etc/systemd/system/watertracker.service > /dev/null <<EOF
[Unit]
Description=WaterTracker FastAPI Server
After=network.target postgresql.service

[Service]
WorkingDirectory=/root/se-toolkit-hackathon/backend
ExecStart=/root/se-toolkit-hackathon/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now watertracker
```

