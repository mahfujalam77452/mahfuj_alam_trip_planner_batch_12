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
### Run test case

create a new bash terminal and run :

```bash
  python test.py
```
## API Endpoints

Health check:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check whether the application is running |

Trip and related resources use the `/api/v1` base URL:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/trips` | Create a trip |
| GET | `/api/v1/trips` | List all trips |
| GET | `/api/v1/trips/<id>` | Get one trip |
| PUT | `/api/v1/trips/<id>` | Update a trip |
| DELETE | `/api/v1/trips/<id>` | Delete a trip |
| POST | `/api/v1/trips/<id>/travelers` | Add a traveler to a trip |
| DELETE | `/api/v1/trips/<id>/travelers/<traveler_id>` | Remove a traveler from a trip |
| POST | `/api/v1/trips/<id>/expenses` | Add an expense to a trip |
| PATCH | `/api/v1/trips/<id>/status` | Change trip status |
| GET | `/api/v1/trips/<id>/summary` | Get calculated trip summary |

## Examples

### Health Check

```http
GET /health
```

Response:

```json
{
  "success": true,
  "status": "ok"
}
```

### Create Trip

```http
POST /api/v1/trips
Content-Type: application/json
```

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

### Add Traveler

```http
POST /api/v1/trips/1/travelers
Content-Type: application/json
```

```json
{
  "name": "Ayesha Rahman",
  "email": "ayesha@example.com"
}
```

Response:

```json
{
  "success": true,
  "message": "you are added in this trip successfully !",
  "data": {
    "id": 1,
    "name": "Ayesha Rahman",
    "email": "ayesha@example.com"
  }
}
```

### Add Expense

```http
POST /api/v1/trips/1/expenses
Content-Type: application/json
```

```json
{
  "title": "Hotel",
  "amount": 12000
}
```

Response:

```json
{
  "success": true,
  "message": "expense added sucessfully",
  "data": {
    "id": 1,
    "trip_id": 1,
    "title": "Hotel",
    "amount": 12000
  }
}
```

### Change Trip Status

```http
PATCH /api/v1/trips/1/status
Content-Type: application/json
```

```json
{
  "status": "ONGOING"
}
```

Response:

```json
{
  "success": true,
  "message": "status updated successfully"
}
```

### Trip Summary

```http
GET /api/v1/trips/1/summary
```

Response:

```json
{
  "destination": "Cox's Bazar",
  "date_of_trip": "2026-11-10",
  "traveler_count": 1,
  "available_seats": 9,
  "total_expense": 12000,
  "remaining_budget": 38000
}
```

### Error Response

Invalid business operations return a non-2xx status. For example, adding an
expense above the remaining budget returns `409 Conflict`:

```json
{
  "error": "Conflict",
  "message": "Your expense is exceeding the total budget"
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

## Assumptions

1. There are no sign-in or sign-up business rules. Therefore, a traveler is
   registered in the system on their first attempt to join a trip, even if
   they are ultimately unable to join that trip because of a business-rule
   conflict.
2. An admin may create the same trip multiple times because the same
   destination and date range may be conducted by different guides.


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