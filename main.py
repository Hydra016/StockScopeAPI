from fastapi import FastAPI
from utils.db import Base, engine
# from tasks.router import task_router
# from user.router import user_router

Base.metadata.create_all(engine)
app = FastAPI(title="SoftScope")
# app.include_router(user_router)
# app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}