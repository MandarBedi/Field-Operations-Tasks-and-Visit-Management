# Field-Operations-Tasks-and-Visit-Management
Its assignment given by Saksham Udaan Fellowship Program that implemented by Sapio Analytics Pvt Ltd. Its Full-stack implementation of the Field Operations Task and Visit Management assignment using Django, Django REST Framework, JWT authentication, PostgreSQL and React with Vite.


## Features

- Role-aware access for `Admin`, `Regional Manager`, `Team Lead`, `Field Agent`, and `Auditor`
- Self-registration for all roles except `Admin`
- Scope-based task, visit, and activity-log visibility
- Task assignment and status transitions
- Field-agent visit start and completion workflows
- Mock AI processing of visit notes with stored structured output
- Dashboard metrics and analytical reporting endpoints
- Demo seed command with ready-to-use sample credentials

## Steps to Run the Project Locally

---

### STEP 1 — CREATE POSTGRESQL DATABASE

Open pgAdmin or psql and run:
```sql
CREATE DATABASE fieldops_db;
```

---

### STEP 2 — SETUP BACKEND

Open Terminal 1 and run these commands ONE BY ONE:

```bash

# Create virtual environment in folder named 'backend'
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies into virtual environment
pip install -r requirements.txt

```

Now open the .env file and fill in your PostgreSQL password:
```
DB_PASSWORD=your_actual_postgres_password
```

Then continue:
```bash
# Run database migrations
python manage.py makemigrations users
python manage.py makemigrations tasks
python manage.py makemigrations visits
python manage.py makemigrations activity
python manage.py makemigrations ai_engine
python manage.py migrate

# Load seed data (creates all test users)
python manage.py seed

# Start the backend server
python manage.py runserver
```

Backend is now running at: http://localhost:8000

---

### STEP 3 — SETUP FRONTEND

Open Terminal 2 (NEW terminal window) and run:

```bash
# Install node packages
npm install

# Start frontend
npm run dev
```
## Demo Credentials

All seeded users share the same password: `Admin@1234`

- `admin` - Admin
- `regional_manager` - Regional Manager
- `south_manager` - Regional Manager
- `team_lead` - Team Lead
- `south_lead` - Team Lead
- `agent_one` - Field Agent
- `agent_two` - Field Agent
- `south_agent` - Field Agent
- `auditor` - Auditor

The frontend login page also exposes these demo users through clickable chips after the backend has been seeded.

## Key API Endpoints

### Auth

- `POST /api/auth/login/`
- `POST /api/auth/register/`
- `POST /api/auth/refresh/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/auth/demo-users/`

### Registration Metadata

- `GET /api/meta/regions/`
- `GET /api/meta/teams/?region_id=<id>`
- `GET /api/meta/managers/`

### Tasks

- `GET /api/tasks/`
- `POST /api/tasks/`
- `GET /api/tasks/{id}/`
- `PATCH /api/tasks/{id}/assign/`
- `PATCH /api/tasks/{id}/status/`

### Visits

- `GET /api/visits/`
- `POST /api/visits/`
- `GET /api/visits/{id}/`
- `PATCH /api/visits/{id}/complete/`
- `PATCH /api/visits/{id}/notes/`

### Reports

- `GET /api/dashboard/`
- `GET /api/reports/logs/`
- `GET /api/reports/tasks/`
- `GET /api/reports/visits-last-7-days/`

## Notes and Tradeoffs

- SQLite is used for local simplicity, though the PRD prefers PostgreSQL.
- The mocked AI service is deterministic and keyword-driven so it can be swapped for a real provider later.
- The React frontend is intentionally functional rather than highly polished.
- List endpoints use DRF page-number pagination (`results`, `count`, `next`, `previous`).