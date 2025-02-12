# db.py
import motor.motor_asyncio
from beanie import init_beanie
from dotenv import load_dotenv
import os
from pathlib import Path
from .models import UserDocument  # Import all models here

# Load environment variables from local .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# MongoDB Atlas connection URI from environment variable
connection_string = os.getenv("MONGODB_URI")

# MongoDB connection URI
client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
database = client["mydatabase"]

# Beanie initialization
async def init():
    # Initialize Beanie with the database and all the document models
    await init_beanie(database, document_models=[UserDocument])


# Function to get the next sequence value
async def get_next_sequence_value(sequence_name: str) -> int:
    counter = await database.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence_value"]