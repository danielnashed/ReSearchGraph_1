from fastapi import FastAPI
from .routes import users, clusters, scheduler
from .middleware import setup_middleware
from .db import init as init_db
from requests.exceptions import RequestException

app = FastAPI(title="Execution Agent API")

setup_middleware(app)
app.include_router(users.router)
app.include_router(clusters.router)
app.include_router(scheduler.router)

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie
    print("Database connected")

@app.get("/")
def read_root():
    return {"message": "Welcome to User Service API!"}