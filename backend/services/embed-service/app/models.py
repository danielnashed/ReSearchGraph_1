from pydantic import BaseModel
from beanie import Document
from typing import Dict, List
from datetime import datetime
from incdbscan import IncrementalDBSCAN

class Paper(BaseModel):
    collection_id: str
    user_id: str
    arxiv_id: str
    title: str
    authors: list
    abstract: str
    published: datetime
    category: str
    url: str
    pdf_url: str
    summary_embedding: List
    fetched_at: datetime = None

class PaperDocument(Paper, Document):
    pass
    class Settings:
        name = "papers"  # MongoDB collection name

class User(BaseModel):
    auto_increment_id: int
    clusterer: bytes
    created_at: datetime = None  # Automatically set when a user is created

    class Config:
        arbitrary_types_allowed = True

class UserDocument(User, Document):
    pass
    class Settings:
        name = "users"  # MongoDB collection name