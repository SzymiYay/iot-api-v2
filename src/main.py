from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.auth import router as auth_router
from src.users import router as user_router
from src.measurements import router as measurement_router
from src import docs

import uvicorn
import os
import urllib
import sqlalchemy
import databases


load_dotenv(".env")

app = FastAPI(
    title="Temperature API",
    description=docs.get_description(),
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": ""
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }

)

host_server = os.environ.get('HOST_SERVER', 'localhost')
db_server_post = urllib.parse.quote_plus(os.environ.get('DB_SERVER_PORT', '5432'))
database_name = os.environ.get('DATABASE_NAME', 'iot_db')
db_username = urllib.parse.quote_plus(os.environ.get('DB_USERNAME', 'postgres'))
db_password = urllib.parse.quote_plus(os.environ.get('DB_PASSWORD', 'postgres'))
ssl_mode = urllib.parse.quote_plus(os.environ.get('SSL_MODE', 'prefer'))
DATABASE_URL = f'postgresql://{db_username}:{db_password}@{host_server}:{db_server_post}/{database_name}?sslmode={ssl_mode}'

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("disabled", sqlalchemy.Boolean),
    sqlalchemy.Column("time_created", sqlalchemy.DateTime),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime),
)

measurements = sqlalchemy.Table(
    "measurements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("temperature", sqlalchemy.Float),
    sqlalchemy.Column("time_created", sqlalchemy.DateTime),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime),
    sqlalchemy.Column("device_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("devices.id")),
)

devices = sqlalchemy.Table(
    "devices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("time_created", sqlalchemy.DateTime),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
metadata.create_all(engine)

database = databases.Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router.router, tags=["Users"])
app.include_router(measurement_router.router, tags=["Measurements"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)