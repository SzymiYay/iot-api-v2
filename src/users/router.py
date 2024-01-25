from fastapi import Depends, status, APIRouter
from azure.iot.hub import IoTHubRegistryManager
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import parse
from hmac import HMAC
import uuid

from src.users import schemas as user_schema

from src.utils import jwt_util
from src.users import crud as user_crud

from src.logger import logger

# Dane do połączenia
iothub_connection_str = "HostName=IOTprojekt.azure-devices.net;SharedAccessKeyName=API;SharedAccessKey=jgzHre8mmua7L74zjb2Ji54dwts4faCiyAIoTD26ics="

# Tworzenie klienta IoT Hub
registry_manager = IoTHubRegistryManager(iothub_connection_str)

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
async def create_device(device_name: str, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    
    def generate_sas_token(uri, key, policy_name=None, expiry=14400000):
        ttl = time() + expiry
        sign_key = "%s\n%d" % ((parse.quote_plus(uri)), int(ttl))
        print(sign_key)
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())

        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(ttl))
        }

        if policy_name is not None:
            rawtoken['skn'] = policy_name 

        return 'SharedAccessSignature ' + parse.urlencode(rawtoken)
    
    device_name = str(uuid.uuid4())
    
    device = registry_manager.create_device_with_sas(device_name, primary_key=None, secondary_key=None, status='enabled')
    primary_key = device.authentication.symmetric_key.primary_key if device.authentication.symmetric_key else None
    sas_token = generate_sas_token(f"IOTprojekt.azure-devices.net/devices/{device_name}", primary_key)
    db_device = user_crud.create_device(device, current_user.id)
    return {"message": "Device created successfully", "id": db_device.id, "name": db_device.name, "primary_key": primary_key, "sas_token": sas_token}


@router.delete("/users/devices/{device_id}", 
            tags=["Users"],
            status_code=status.HTTP_200_OK,
            response_description="Device deleted successfully")
async def delete_device(device_name: str, current_user: user_schema.User = Depends(jwt_util.get_current_active_user)):
    # db_device = user_crud.delete_device(device_id)
    db_device = user_crud.delete_device_by_name(device_name)
    registry_manager.delete_device(device_name)
    return {"message": "Device deleted successfully", "name": db_device.name}
