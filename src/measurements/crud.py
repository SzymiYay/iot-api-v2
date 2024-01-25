from fastapi_sqlalchemy import db

from src.measurements import schemas
from src.users import crud as user_crud
from src import models as measurement_model

from src import logger as app_logger

logger = app_logger.get_logger()


def create_measurement(measurement: schemas.Measurement):
    db_device = user_crud.get_device_by_name(measurement.device_name)
    db_measurement = measurement_model.Measurement(temperature=measurement.temperature, device_name=db_device.name)
    db.session.add(db_measurement)
    db.session.commit()
    return db_measurement


def get_measurement(measurement_id: int):
    db_measurement = db.session.query(measurement_model.Measurement).filter(measurement_model.Measurement.id == measurement_id).first()
    return db_measurement


def get_measurements():
    db_measurements = db.session.query(measurement_model.Measurement).all()
    return db_measurements


def get_measurements_by_device(device_name: str):
    db_measurements = db.session.query(measurement_model.Measurement).filter(measurement_model.Measurement.device_name == device_name).all()
    return db_measurements
