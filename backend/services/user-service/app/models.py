from pydantic import BaseModel
from beanie import Document
from typing import Dict, List
from datetime import datetime

class Cluster(BaseModel):
    cluster_id: float
    user_id: str
    label: str
    summary: list
    summary_embedding: List
    papers: list
    updated_at: datetime = None

class ClusterDocument(Cluster, Document):
    pass
    class Settings:
        name = "clusters"  # MongoDB collection name

class User(BaseModel):
    auto_increment_id: int
    email: str
    password: str
    clusterer: bytes
    created_at: datetime = None  # Automatically set when a user is created

    class Config:
        arbitrary_types_allowed = True

class UserDocument(User, Document):
    pass
    class Settings:
        name = "users"  # MongoDB collection name