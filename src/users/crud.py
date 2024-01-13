from fastapi import HTTPException, status
from fastapi_sqlalchemy import db

from src import models
from src.users import schemas

def deactivate_account(user_id: int):
    db_user = db.session.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_devices = db.session.query(models.Device).filter(models.Device.user_id == user_id).all()
    db_devices_id = [db_device.id for db_device in db_devices]

    db_measurements = db.session.query(models.Measurement).filter(models.Measurement.device_id.in_(db_devices_id)).all()
    for db_measurement in db_measurements:
        db.session.delete(db_measurement)
    
    for db_device in db_devices:
        db.session.delete(db_device)

    db_tokens = db.session.query(models.Token).filter(models.Token.user_id == user_id).all()
    for db_token in db_tokens:
        db.session.delete(db_token)
    
    db.session.delete(db_user)
    db.session.commit()


def get_devices(user_id: int):
    db_devices = db.session.query(models.Device).filter(models.Device.user_id == user_id).all()
    return db_devices


def get_device(device_id: int):
    db_device = db.session.query(models.Device).filter(models.Device.id == device_id).first()

    if not db_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    return db_device


def create_device(device: schemas.Device, user_id: int):
    db_device = models.Device(name=device.name, user_id=user_id)
    db.session.add(db_device)
    db.session.commit()
    return db_device


def delete_device(device_id: int):
    db_device = db.session.query(models.Device).filter(models.Device.id == device_id).first()

    if not db_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    
    db.session.delete(db_device)
    db.session.commit()
    return db_device
