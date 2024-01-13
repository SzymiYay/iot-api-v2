from fastapi import Depends, status, APIRouter

from src.users import schemas as user_schema

from src.utils import jwt_util
from src.users import crud as user_crud

router = APIRouter(
    prefix="/api/v1",
    tags=["Users"]
)

@router.get("/users/profile", 
         response_model=user_schema.User, 
         tags=["Users"],
         status_code=status.HTTP_200_OK,
         response_description="User details")
async def get_user_profile(current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    return current_user


@router.delete("/users",
            tags=["Users"],
            status_code=status.HTTP_200_OK,
            response_description="User deleted successfully")
async def deactivate_account(current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    user_crud.deactivate_account(current_user.id)
    return {"message": "User account deactivated successfully"}


@router.get("/users/devices", 
         response_model=list[user_schema.DeviceReturn], 
         tags=["Users"],
         status_code=status.HTTP_200_OK,
         response_description="User devices")
async def get_devices(current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_devices = user_crud.get_devices(current_user.id)
    return db_devices


@router.post("/users/devices", 
          tags=["Users"],
          status_code=status.HTTP_201_CREATED,
          response_description="Device created successfully")
async def create_device(device: user_schema.Device, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_device = user_crud.create_device(device, current_user.id)
    return {"message": "Device created successfully", "name": db_device.name}


@router.delete("/users/devices/{device_id}", 
            tags=["Users"],
            status_code=status.HTTP_200_OK,
            response_description="Device deleted successfully")
async def delete_device(device_id: int, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    db_device = user_crud.delete_device(device_id)
    return {"message": "Device deleted successfully", "name": db_device.name}
