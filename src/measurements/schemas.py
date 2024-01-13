from pydantic import BaseModel
from datetime import datetime

class Measurement(BaseModel):
    temperature: float
    device_id: int

class MeasurementReturn(Measurement):
    time_created: datetime

class MeasurementInDB(Measurement):
    id: int
    time_created: datetime
    time_updated: datetime
    device_id: int

    class Config:
        orm_mode = True