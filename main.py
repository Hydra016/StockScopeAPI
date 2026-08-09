from fastapi import FastAPI
from utils.db import Base, engine
from routes.users import user_router
from routes.auth import auth_router
from routes.stocks import stock_router
from routes.admin import admin_router

Base.metadata.create_all(engine)
app = FastAPI(title="SoftScope")
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(admin_router)