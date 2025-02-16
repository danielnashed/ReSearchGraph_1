from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..crud import ClusterCRUD as CRUD
from pydantic import BaseModel

router = APIRouter(prefix="/clusters", tags=["Clusters"])

# Get all clusters for a specific user by user ID
@router.get("/{user_id}")
async def get_clusters_route(user_id: str):
    clusters = await CRUD.get_clusters(user_id)
    cluster_data = []
    for cluster in clusters:
        cluster_data.append({
            "title": cluster.label,
            "summary": cluster.summary,
            "papers": cluster.papers,
            "papers_count": len(cluster.papers)
        })
    return JSONResponse(content={"clusters": cluster_data}, 
                        status_code=200)