# Smart Group Trip Planner API

A Flask and SQLAlchemy based API for managing group trips, including trip dates, budget, traveler capacity, expenses, and status.

## Prerequisites

- Python 3
- Git
- Bash

## Run

For a fresh clone:

```bash
git clone https://github.com/mahfujalam77452/mahfuj_alam_trip_planner_batch_12
cd mahfuj_alam_trip_planner_batch_12
chmod +x run.sh
./run.sh
```

`run.sh` automatically creates the virtual environment, installs dependencies, creates `.env` from `.env.example`, and starts the API.

API URL:

```text
http://127.0.0.1:5000
```

### Manual Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

## API Endpoints

Base URL: `/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/trips` | Create trip |
| GET | `/trips` | List trips |
| GET | `/trips/<id>` | Get trip |
| PUT | `/trips/<id>` | Update trip |
| DELETE | `/trips/<id>` | Delete trip |

Health check: `GET /helth`

## Example

### Create Trip

```json
{
  "destination": "Cox's Bazar",
  "start_date": "2026-11-10",
  "end_date": "2026-11-14",
  "budget": 50000,
  "max_travelers": 10
}
```

Response:

```json
{
  "success": true,
  "message": "Trip created successfully",
  "data": {
    "id": 1,
    "destination": "Cox's Bazar",
    "budget": 50000,
    "max_travelers": 10,
    "current_travelers": 0,
    "expenses": 0,
    "status": "PLANNED"
  }
}
```

## Business Rules

- Start date cannot be after end date.
- Budget and maximum capacity must be greater than zero.
- Traveler capacity cannot be exceeded.
- Duplicate participation is not allowed.
- A traveler cannot have overlapping trips.
- Expenses cannot exceed the trip budget.
- Only valid status transitions are allowed.

## Project Structure

```text
.
├── run.sh
├── run.py
├── requirements.txt
├── .env.example
└── app/
    ├── config.py
    ├── extensions.py
    ├── models/
    ├── schemas/
    ├── controllers/
    └── routes/
```

## SQLite

The project uses SQLite.

```env
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

Database tables are initialized automatically when the application starts.

`.env` and the local SQLite database are not committed to the repository.