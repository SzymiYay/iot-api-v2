from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from src.auth import router as auth_router
from src.users import router as user_router
from src.measurements import router as measurement_router
from src import docs
from sqlalchemy import text

import os
import urllib
import sqlalchemy
import uvicorn
import databases

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
    sqlalchemy.Column("device_id", sqlalchemy.String, sqlalchemy.ForeignKey("devices.id")),
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

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(user_router.router, tags=["Users"])
app.include_router(measurement_router.router, tags=["Measurements"])


# import paho.mqtt.client as mqtt
# import ssl

# def on_connect(client, userdata, flags, rc):
#     print(f"Connected with result code {rc}")
#     topic = "$iothub/device1/messages/devicebound/#"
#     mqtt_client.subscribe(topic)

# def on_subscribe(client, userdata, mid, granted_qos):
#     print(f"Subscribed with QoS: {granted_qos}")

# def on_message(client, userdata, msg):
#     print(f"Received message: {msg.payload}")

# def on_publish(client, userdata, mid):
#     print(f"Message published with id: {mid}")

# def on_disconnect(client, userdata, rc):
#     if rc != 0:
#         print(f"Unexpected disconnection: {rc}\n")
#         print(" ")


# mqtt_client = mqtt.Client(client_id='device1', protocol=mqtt.MQTTv311)
# mqtt_client.on_connect = on_connect
# mqtt_client.on_subscribe = on_subscribe
# mqtt_client.on_message = on_message
# mqtt_client.on_publish = on_publish
# mqtt_client.on_disconnect = on_disconnect
# mqtt_client.username_pw_set(username="IOTprojekt.azure-devices.net/device1/?api-version=2021-04-12", password="SharedAccessSignature sr=IOTprojekt.azure-devices.net%2Fdevices%2Fdevice1&sig=fcIQpH8Vo6eRSFH5sO80tUjFcojToevYxlJtKuEQAWs%3D&se=1708636469")

# mqtt_client.tls_set(ca_certs=r"C:\Users\szymo\Desktop\Studia\Semestr 5\IOT\iot-api-v2\cert.cer", certfile=None, keyfile=None,
#                cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# mqtt_client.tls_insecure_set(True)

# mqtt_client.connect("IOTprojekt.azure-devices.net", port=8883)
# mqtt_client.loop_start()

# mqtt_client.publish("devices/device1/messages/events/", '{"id":123}', qos=1)

# mqtt_client.loop_forever()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)