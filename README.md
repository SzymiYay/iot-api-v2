# IOT Project - api

- [Prerequisites](#prerequisites)
    - [Tools](#tools)
    - [Languages](#languages)
- [Basics of the project](#basics-of-the-project)
  - [Architecture](#architecture)
- [Usage](#usage)
  - [Run locally](#run-locally)
    - [Virtual environment](#virtual-environment)
      - [Create](#create)
      - [Activate](#activate)
    - [Install dependencies](#install-dependencies)
    - [Create alembic](#create-alembic)
    - [Run](#run)
    - [Migrations](#migrations)
    - [Local development](#local-development)

## Prerequisites
Scripts are written for all platforms, but they were tested only on Windows 11.

### Tools
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/)

## Basics of the project
### Architecture
Project consists of 1 microservice:
- **FastAPI** service that provides REST API that allows us to get data about measurements from the connected devices.

```json
// GET
// /api/v1/users/devices
[
    {
        "id": 1,
        "name": "your_device_name",
        "user_id": 1
    }
]

```


```json
// GET
// /api/v1/measurements
[
    {
        "temperature": 20,
        "time_created": "2021-01-01T00:00:00+00:00",
        "device_id": 1
    }
]
```
## Run locally

### One command setup
1. Docker Desktop must be running
2. Open Git Bash
3. Run command
```bash
./run.sh
```

### Each step of setup

### Virtual environment
#### Create
```bash
python -m venv venv
```
#### Activate
```bash
 ./venv/Scripts/activate
```

### Install dependencies
```bash
pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv python-multipart python-jose[cryptography] passlib[bcrypt] python-multipart
```

### Create alembic
```bash
alembic init alembic
```

### Run
```bash
docker-compose build
docker-compose up
```

### Migrations
```bash
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head
```

### Local development
```bash
uvicorn src.main:app --reload
```

### API documentation
```bash
http://localhost:8000/docs
```

### PGAdmin
```bash
http://localhost:5050
```
1. Login
```bash
email: admin@admin.com
password: admin
```
2. Add new server
```bash
host: db
name: db
port: 5432
username: postgres
password: password
```






