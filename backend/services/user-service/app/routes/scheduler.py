from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..aws.eventbridge_client import EventBridgeClient

router = APIRouter(prefix="/scheduler", tags=["Scheduler"])

class PostRequest(BaseModel):
    scheduler_on: bool

# Set fetch papers scheduler for a specific user by user ID
@router.post("/{user_id}")
async def get_clusters_route(user_id: str, request: PostRequest):
    eventbridge_client = EventBridgeClient(rule=f"FetchPapersScheduledRule_{user_id}")
    if request.scheduler_on:
        eventbridge_client.enable_rule()
        return JSONResponse(content={"data": 'scheduler enabled'}, 
                        status_code=200)
    else:
        eventbridge_client.disable_rule()
        return JSONResponse(content={"data": 'scheduler disabled'}, 
                            status_code=200)