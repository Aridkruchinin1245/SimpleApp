from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import create_tables
from backend.routers import utils_routes, post_routes, auth_reg_routes

app = FastAPI()

app.include_router(router=utils_routes.router)
app.include_router(router=post_routes.router)
app.include_router(router=auth_reg_routes.router)

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
