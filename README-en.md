# FastAPI CRUD Demo

[中文](./README.md)

A user CRUD API demo built with FastAPI + SQLAlchemy + MySQL.

## Project Structure

```
fastapi-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory & lifespan
│   ├── config.py                # pydantic-settings config (reads .env)
│   ├── database.py              # SQLAlchemy engine / session / Base / get_db
│   ├── api/
│   │   ├── response_route.py    # Custom APIRoute for unified ApiResponse wrapping
│   │   └── v1/
│   │       ├── router.py        # v1 route aggregation
│   │       ├── users.py         # User CRUD endpoints
│   │       └── roles.py         # Role CRUD endpoints
│   ├── models/
│   │   ├── __init__.py          # Model imports (for create_all)
│   │   ├── user.py              # SQLAlchemy User ORM model
│   │   └── role.py              # SQLAlchemy Role ORM model
│   ├── schemas/
│   │   ├── response.py          # ApiResponse generic response model
│   │   ├── user.py              # Pydantic v2: UserCreate/UserUpdate/UserResponse/UserFilter
│   │   └── role.py              # Pydantic v2: RoleCreate/RoleUpdate/RoleResponse/RoleFilter
│   ├── services/
│   │   ├── user.py              # User business logic
│   │   └── role.py              # Role business logic
│   └── exceptions/
│       └── handlers.py          # Custom exceptions & global handlers
├── pyproject.toml               # Project metadata & dependencies
├── .env                         # Environment variables
└── README.md
```

## Tech Stack

| Component        | Choice            |
|------------------|-------------------|
| Web Framework    | FastAPI           |
| ORM              | SQLAlchemy 2.0    |
| Database         | MySQL (PyMySQL)   |
| Data Validation  | Pydantic v2       |
| Config Management| pydantic-settings |

## Quick Start

### Prerequisites

- Python >= 3.10
- MySQL server

### 1. Install dependencies

```bash
pip install -e .
```

### 2. Configure database

Edit `.env` with your MySQL connection info:

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
```

Create the database if it doesn't exist:

```bash
mysql -u user -p -e "CREATE DATABASE IF NOT EXISTS dbname CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Start the server

```bash
python -m app.main
```

Once started:
- API docs: http://127.0.0.1:3002/docs
- ReDoc: http://127.0.0.1:3002/redoc

### PyCharm Debugging

1. Open PyCharm, click **Add Configuration...** → **+** → **Python**
2. Configure as follows:

| Field        | Value                           |
|--------------|---------------------------------|
| Name         | `FastAPI Debug`                 |
| Module name  | `app.main`                      |
| Working dir  | Project root (fastapi-demo)     |

3. Set breakpoints in the code, then click **Debug** to start debugging

> Make sure the Python interpreter used by PyCharm has project dependencies installed.

### SQL Logging

Set `DEBUG=true` in `.env` during development to print all SQL statements in the terminal.

## API Endpoints

### User Endpoints

All endpoints prefixed with: `/api/v1/users`

| Method | Path         | Description     | Parameters                                                           |
|--------|-------------|-----------------|----------------------------------------------------------------------|
| POST   | `/`          | Create user     | Body: UserCreate JSON                                                |
| GET    | `/`          | List users      | Query: `skip`(default 0), `limit`(default 100), `name`(fuzzy), `age`(exact) |
| GET    | `/{user_id}` | Get user        | Path: user_id                                                        |
| PUT    | `/{user_id}` | Update user     | Path: user_id, Body: UserUpdate JSON                                 |
| DELETE | `/{user_id}` | Delete user     | Path: user_id                                                        |

### Role Endpoints

All endpoints prefixed with: `/api/v1/roles`

| Method | Path         | Description     | Parameters                                                      |
|--------|-------------|-----------------|-----------------------------------------------------------------|
| POST   | `/`          | Create role     | Body: RoleCreate JSON                                           |
| GET    | `/`          | List roles      | Query: `skip`(default 0), `limit`(default 100), `name`(fuzzy)   |
| GET    | `/{role_id}` | Get role        | Path: role_id                                                   |
| PUT    | `/{role_id}` | Update role     | Path: role_id, Body: RoleUpdate JSON                            |
| DELETE | `/{role_id}` | Delete role     | Path: role_id                                                   |

## Request Examples

**Create user:**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Zhang San", "email": "zhangsan@example.com", "age": 28}'
```

**List users (paginated + filtered):**
```bash
curl "http://127.0.0.1:3002/api/v1/users/?skip=0&limit=10&name=Zhang&age=28"
```

**Get single user:**
```bash
curl "http://127.0.0.1:3002/api/v1/users/1"
```

**Partial update:**
```bash
curl -X PUT "http://127.0.0.1:3002/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Li Si"}'
```

**Create role:**
```bash
curl -X POST "http://127.0.0.1:3002/api/v1/roles/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Admin", "description": "System administrator"}'
```

**List roles:**
```bash
curl "http://127.0.0.1:3002/api/v1/roles/?name=Admin"
```

**Delete user:**
```bash
curl -X DELETE "http://127.0.0.1:3002/api/v1/users/1"
```

## Response Status Codes

| Status code | Meaning               |
|-------------|-----------------------|
| 200         | OK                    |
| 201         | Created               |
| 204         | No Content            |
| 400         | Bad Request           |
| 404         | Not Found             |
| 409         | Conflict              |
| 422         | Validation Error      |
| 500         | Internal Server Error |

## User Fields

| Field      | Type     | Description                    |
|------------|----------|--------------------------------|
| id         | int      | Primary key, auto-increment    |
| name       | string   | Name, 1-100 characters         |
| email      | string   | Email, unique                  |
| age        | int      | Age, 0-150, optional           |
| role_id    | int      | Role ID, optional              |
| created_at | datetime | Creation time (auto)           |
| updated_at | datetime | Update time (auto)             |

## Role Fields

| Field       | Type     | Description                    |
|-------------|----------|--------------------------------|
| id          | int      | Primary key, auto-increment    |
| name        | string   | Role name, 1-50 chars, unique  |
| description | string   | Description, 0-200 chars, optional |
| created_at  | datetime | Creation time (auto)           |
| updated_at  | datetime | Update time (auto)             |

## Response Format

All endpoints return a unified JSON structure:

```json
{
  "code": 200,
  "message": "OK",
  "data": { ... }
}
```

## Architecture

```
HTTP Request
    │
    ▼
Router (app/api/v1/users.py)  —— parse params, call service
    │
    ▼
Service (app/services/user.py) —— business logic, transaction management
    │
    ▼
Model (app/models/user.py) —— SQLAlchemy ORM
    │
    ▼
MySQL
```

Exceptions are caught by `app/exceptions/handlers.py` and returned as standardized JSON error responses.

## License

[MIT](LICENSE)
