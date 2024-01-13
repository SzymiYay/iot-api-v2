from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from src.auth import router as auth_router
from src.users import router as user_router
from src.measurements import router as measurement_router
from src import docs

from src.db_config import database, DATABASE_URL


import uvicorn


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)