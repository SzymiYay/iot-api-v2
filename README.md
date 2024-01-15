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
    - [Run](#run)

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
pip install -r requirements.txt
```

### Run
```bash
uvicorn src.main:app --reload
```
