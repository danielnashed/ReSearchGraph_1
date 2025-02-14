from datetime import datetime
from typing import Optional, List
from .models import UserDocument, PaperDocument
from fastapi import HTTPException
from bson import ObjectId
from .db import get_next_sequence_value

class UserCRUD():
    # Create a new user
    @staticmethod
    async def create_user() -> UserDocument:
        auto_increment_id = await get_next_sequence_value("user_id")
        new_user = UserDocument(auto_increment_id=auto_increment_id,
                                created_at=datetime.now())
        await new_user.insert()
        return new_user
    
    # Get a user by ID
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserDocument]:
        return await UserDocument.find_one({"_id": ObjectId(user_id)})
    
    # Delete a user by ID
    @staticmethod
    async def delete_user(user_id: str) -> dict:
        existing_user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if existing_user:
            await existing_user.delete()
            return {"message": "User deleted"}
        return {"message": "User not found"}
    

class paperCRUD():
    # Create a new paper
    @staticmethod
    async def create_paper(paper: dict) -> PaperDocument:
        # Ensure the user exists
        user_id = paper.get("user_id")
        user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        new_paper = PaperDocument(user_id=user_id,
                                    collection_id=paper.get("collection_id"),
                                    arxiv_id=paper.get("arxiv_id"),
                                    title=paper.get("title"),
                                    authors=paper.get("authors"),
                                    abstract=paper.get("abstract"),
                                    published=paper.get("published"),
                                    category=paper.get("category"),
                                    url=paper.get("url"),
                                    pdf_url=paper.get("pdf_url"),
                                    summary_embedding=[],
                                    fetched_at=datetime.now())
        await new_paper.insert()
        return new_paper
    
    # Get papers by user ID and collection ID
    @staticmethod
    async def get_papers(user_id: str, collection_id: str) -> List[PaperDocument]:
        return await PaperDocument.find({"user_id": user_id, "collection_id": collection_id}).to_list()