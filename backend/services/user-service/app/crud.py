from datetime import datetime
from typing import Optional, List
from .models import UserDocument, ClusterDocument
from fastapi import HTTPException
from bson import ObjectId
from .db import get_next_sequence_value
from incdbscan import IncrementalDBSCAN
from .aws.eventbridge_client import EventBridgeClient
from dotenv import load_dotenv
import pickle
import os

load_dotenv()
AWS_TARGET_ARN = os.getenv("AWS_TARGET_ARN")
AWS_TARGET_ROLE_ARN= os.getenv("AWS_TARGET_ROLE_ARN")

class UserCRUD():
    # Create a new user
    @staticmethod
    async def create_user(email: str, password: str) -> UserDocument:
        auto_increment_id = await get_next_sequence_value("user_id")
        clusterer = IncrementalDBSCAN(eps=0.5, min_pts=5)
        # Serialize the clusterer object
        serialized_clusterer = pickle.dumps(clusterer)
        new_user = UserDocument(auto_increment_id=auto_increment_id,
                                email=email,
                                password=password,
                                clusterer=serialized_clusterer,
                                created_at=datetime.now())
        await new_user.insert()
        # Create an eventbridge rule and target for user
        user = await UserCRUD.get_user_by_email_password(email, password) 
        rule_name = f"FetchPapersScheduledRule_{str(user.id)}"
        target_name = f"FetchPapersScheduledTarget_{str(user.id)}"
        target = {"Id": target_name,
                    "Arn": AWS_TARGET_ARN,
                    "RoleArn": AWS_TARGET_ROLE_ARN,
                  }
        eventbridge_client = EventBridgeClient(rule=rule_name, target=target)
        eventbridge_client.create_rule(schedule="cron(0 9 * * ? *)")                                     
        return new_user
    
    # Get a user by ID
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserDocument]:
        user = await UserDocument.find_one({"_id": ObjectId(user_id)})
        if user:
            # Deserialize the clusterer object
            user.clusterer = pickle.loads(user.clusterer)
        return user
    
    # Get a user by email and password
    @staticmethod
    async def get_user_by_email_password(email: str, password: str) -> Optional[UserDocument]:
        user = await UserDocument.find_one({"email": email, "password": password})
        if user:
            # Deserialize the clusterer object
            user.clusterer = pickle.loads(user.clusterer)
        return user
    
    # Delete a user by ID
    @staticmethod
    async def delete_user(user_id: str) -> dict:
        existing_user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if existing_user:
            await existing_user.delete()
            return {"message": "User deleted"}
        return {"message": "User not found"}


class ClusterCRUD():
    # Get all clusters by user ID
    @staticmethod
    async def get_clusters(user_id: str) -> Optional[ClusterDocument]:
        return await ClusterDocument.find({"user_id": user_id}).to_list()
