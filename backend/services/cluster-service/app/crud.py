from datetime import datetime
from typing import Optional, List
from .models import UserDocument, PaperDocument, ClusterDocument
from fastapi import HTTPException
from bson import ObjectId
from .db import get_next_sequence_value
from incdbscan import IncrementalDBSCAN
import pickle

class UserCRUD():
    # Create a new user
    @staticmethod
    async def create_user() -> UserDocument:
        auto_increment_id = await get_next_sequence_value("user_id")
        clusterer = IncrementalDBSCAN(eps=1.0, min_pts=2)
        # Serialize the clusterer object
        serialized_clusterer = pickle.dumps(clusterer)
        new_user = UserDocument(auto_increment_id=auto_increment_id,
                                clusterer=serialized_clusterer,
                                created_at=datetime.now())
        await new_user.insert()
        return new_user
    
    # Get a user by ID
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserDocument]:
        user = await UserDocument.find_one({"_id": ObjectId(user_id)})
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
                                    arxiv_id=paper.get("arxiv_id"),
                                    title=paper.get("title"),
                                    authors=paper.get("authors"),
                                    abstract=paper.get("abstract"),
                                    published=paper.get("published"),
                                    category=paper.get("category"),
                                    url=paper.get("url"),
                                    pdf_url=paper.get("pdf_url"),
                                    summary_embedding=None,
                                    fetched_at=datetime.now())
        await new_paper.insert()
        return new_paper
    
    # Get paper by ID
    @staticmethod
    async def get_paper(id: str) -> List[PaperDocument]:
        return await PaperDocument.get({"_id": ObjectId(id)})
    
    # Get papers by user ID and collection ID
    @staticmethod
    async def get_papers(user_id: str, collection_id: str) -> List[PaperDocument]:
        return await PaperDocument.find({"user_id": user_id, "collection_id": collection_id}).to_list()
    
    # Get papers by user ID and collection ID
    @staticmethod
    async def get_all_papers(user_id: str) -> List[PaperDocument]:
        return await PaperDocument.find({"user_id": user_id}).to_list()


class clusterCRUD():
    # Create a new cluster of papers
    @staticmethod
    async def create_cluster(cluster: dict) -> ClusterDocument:
        # Ensure the user exists
        user_id = cluster.get("user_id")
        user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        new_cluster = ClusterDocument(user_id=user_id,
                                    cluster_id=cluster.get("cluster_id"),
                                    label=cluster.get("label"),
                                    summary=[cluster.get("summary")],
                                    summary_embedding=[cluster.get("summary_embedding")],
                                    papers=cluster.get("papers"),
                                    updated_at=datetime.now())
        await new_cluster.insert()
        return new_cluster
    
    # Update existing cluster
    @staticmethod
    async def update_cluster(cluster: dict) -> ClusterDocument:
        # Ensure the user exists
        user_id = cluster.get("user_id")
        cluster_id = cluster.get("cluster_id")
        user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cluster = await clusterCRUD.get_cluster(user_id, cluster_id)
        cluster.summary.append(cluster.get("summary"))
        cluster.summary_embedding.append(cluster.get("summary_embedding"))
        cluster.papers.append(cluster.get("papers"))
        cluster.updated_at = datetime.now()
        await cluster.save()
        return cluster
    
    # Get all clusters by user ID
    @staticmethod
    async def get_all_clusters(user_id: str) -> List[ClusterDocument]:
        return await ClusterDocument.find({"user_id": user_id}).to_list()
    
    # Get cluster by user ID and cluster ID
    @staticmethod
    async def get_cluster(user_id: str, cluster_id: str) -> List[ClusterDocument]:
        return await ClusterDocument.find_one({"user_id": user_id, "cluster_id": cluster_id})
    