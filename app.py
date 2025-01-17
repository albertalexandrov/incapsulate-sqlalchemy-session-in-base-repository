from fastapi import FastAPI

from api.router import users_router

app = FastAPI()
app.include_router(users_router)
