# Engineering Dashboard

A full-stack dashboard that monitors real battery and CPU temperature readings from a MacBook and displays recent readings over time.

## Features

- Collects battery charge and charging status from macOS
- Collects average CPU temperature from an Apple Silicon Mac using `macmon`
- Stores readings in PostgreSQL
- Provides a FastAPI REST API
- Displays current readings and history charts
- Removes readings older than 30 days

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Chart.js
- Backend: Python, FastAPI, SQLAlchemy
- Database: PostgreSQL
- Mac telemetry: `pmset` and `macmon`

## Requirements

- macOS on an Apple Silicon Mac
- Python and the project’s `.venv`
- PostgreSQL, with the `engineering_dashboard` database available
- `macmon` installed and working

Install `macmon` with Homebrew if needed:

```bash
brew install macmon
```

## Terminals

### Terminal 1: Backend API

```bash
cd ~/Documents/engineering-dashboard
source .venv/bin/activate
uvicorn backend.main:app --reload
```

### Terminal 2: Frontend 

```bash
cd ~/Documents/engineering-dashboard/frontend
python3 -m http.server 5500
```

### Terminal 3: Battery collector 

```bash
cd ~/Documents/engineering-dashboard
source .venv/bin/activate
python backend/mac_battery.py
```

### Terminal 4: CPU temperature collector 
lets 
```bash
cd ~/Documents/engineering-dashboard
source .venv/bin/activate
python backend/mac_temperature.py
```