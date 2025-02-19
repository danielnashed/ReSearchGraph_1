from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..crud import UserCRUD as CRUD
from pydantic import BaseModel
from ..aws.eventbridge_client import EventBridgeClient
from ..utils import create_target_for_user

router = APIRouter(prefix="/users", tags=["Users"])

class PostRequest(BaseModel):
    email: str
    password: str

# Create a new User
@router.post("/signup")
async def signup_route(request: PostRequest):
    new_user = await CRUD.create_user(email=request.email, password=request.password)
    # Create an eventbridge rule and target for user
    rule_name = f"FetchPapersScheduledRule_{str(new_user.id)}"
    target = create_target_for_user(str(new_user.id))
    print("target is: ", target)
    eventbridge_client = EventBridgeClient(rule=rule_name, target=target)
    eventbridge_client.create_rule(schedule="cron(0 9 * * ? *)")  
    return JSONResponse(content={"user_id": str(new_user.id)}, 
                        status_code=201)

# Get a User by email and password
@router.post("/login")
async def login_route(request: PostRequest):
    user = await CRUD.get_user_by_email_password(email=request.email, password=request.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"user_id": str(user.id)}, 
                        status_code=200)

# Get a User by ID
@router.get("/{user_id}")
async def get_user_route(user_id: str):
    user = await CRUD.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"user_id": str(user.id)}, 
                        status_code=200)

# Delete a User
@router.delete("/{user_id}")
async def delete_user_route(user_id: str):
    result = await CRUD.delete_user(user_id)
    if result.get("message") == "User not found":
        raise HTTPException(status_code=404, detail="User not found")
    # Delete eventbridge rule and target for user
    rule_name = f"FetchPapersScheduledRule_{user_id}"
    target = create_target_for_user(user_id)
    eventbridge_client = EventBridgeClient(rule=rule_name, target=target)
    eventbridge_client.delete_rule()  
    return JSONResponse(content=result, 
                        status_code=200)