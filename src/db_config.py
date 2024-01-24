import os
import urllib
import sqlalchemy
import databases
from sqlalchemy import text

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
    sqlalchemy.Column("time_created", sqlalchemy.DateTime, server_default=text("CURRENT_TIMESTAMP")),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime, onupdate=text("CURRENT_TIMESTAMP")),
)

measurements = sqlalchemy.Table(
    "measurements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("temperature", sqlalchemy.Float),
    sqlalchemy.Column("time_created", sqlalchemy.DateTime, server_default=text("CURRENT_TIMESTAMP")),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime, onupdate=text("CURRENT_TIMESTAMP")),
    sqlalchemy.Column("device_name", sqlalchemy.String, sqlalchemy.ForeignKey("devices.name")),
)

devices = sqlalchemy.Table(
    "devices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("time_created", sqlalchemy.DateTime, server_default=text("CURRENT_TIMESTAMP")),
    sqlalchemy.Column("time_updated", sqlalchemy.DateTime, onupdate=text("CURRENT_TIMESTAMP")),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
metadata.create_all(engine)
database = databases.Database(DATABASE_URL)