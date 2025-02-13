from pydantic import BaseModel
from beanie import Document
from typing import Dict
from datetime import datetime


class User(BaseModel):
    auto_increment_id: int
    created_at: datetime = None  # Automatically set when a user is created

class UserDocument(User, Document):
    auto_increment_id: int
    created_at: datetime
    class Settings:
        name = "users"  # MongoDB collection name