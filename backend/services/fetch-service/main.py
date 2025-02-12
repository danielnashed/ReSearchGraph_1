from fastapi import FastAPI
from app.routes import users
from app.middleware import setup_middleware
from app.db import init as init_db
from requests.exceptions import RequestException

app = FastAPI(title="Execution Agent API")

setup_middleware(app)
app.include_router(users.router)

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie

@app.get("/")
def read_root():
    return {"message": "Welcome to Execution Agent API!"}