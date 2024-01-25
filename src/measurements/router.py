from fastapi import Depends, status, APIRouter

from src.utils import jwt_util
from src.measurements import schemas as measurement_schema
from src.users import schemas as user_schema
from src.measurements import crud as measurement_crud


router = APIRouter(
    prefix="/api/v1",
    tags=["Measurements"]
)

@router.post("/measurements", 
          tags=["Measurements"],
          status_code=status.HTTP_201_CREATED,
          response_description="Measurement created successfully")
async def create_measurement(measurement: measurement_schema.Measurement, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_measurement = measurement_crud.create_measurement(measurement)
    return {"message": "Measurement created successfully", "temperature": db_measurement.temperature}


@router.get("/measurements/{measurement_id}", 
         response_model=measurement_schema.MeasurementReturn, 
         tags=["Measurements"],
         status_code=status.HTTP_200_OK,
         response_description="Measurement details")
async def get_measurement(measurement_id: int, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_measurement = measurement_crud.get_measurement(measurement_id)
    return db_measurement


@router.get("/measurements", 
         response_model=list[measurement_schema.MeasurementReturn], 
         tags=["Measurements"],
         status_code=status.HTTP_200_OK,
         response_description="Measurements")
async def get_measurements(current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_measurements = measurement_crud.get_measurements()
    return db_measurements


@router.get("/measurements/devices/{device_id}",
            response_model=list[measurement_schema.MeasurementReturn],
            tags=["Measurements"],
            status_code=status.HTTP_200_OK,
            response_description="Measurements")
async def get_measurements_by_device_id(device_name: str, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_measurements = measurement_crud.get_measurements_by_device(device_name)
    return db_measurements
