from fastapi import FastAPI
from .routes import users, papers
from .middleware import setup_middleware
from .db import init as init_db
from requests.exceptions import RequestException

app = FastAPI(title="Fetch Service API")

setup_middleware(app)
app.include_router(users.router)
app.include_router(papers.router)

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie
    print("Database connected")

@app.get("/")
def read_root():
    return {"message": "Welcome to Fetch Service API!"}