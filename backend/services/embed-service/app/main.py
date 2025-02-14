from fastapi import FastAPI
from .routes import users
from .middleware import setup_middleware
from .db import init as init_db
from requests.exceptions import RequestException
from .aws.sqs_client import SQSClient
from .utils import create_embeddings
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

app = FastAPI(title="Execution Agent API")

setup_middleware(app)
app.include_router(users.router)

# Initialize the SQS client for input and output queues
cluster_queue_url = os.getenv('AWS_SQS_CLUSTER_URL')
cluster_sqs_client = SQSClient(cluster_queue_url)
embed_queue_url = os.getenv('AWS_SQS_EMBED_URL')
embed_sqs_client = SQSClient(embed_queue_url, 
                             process_message=create_embeddings, 
                             consumer=cluster_sqs_client
                             )

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie
    print("Database connected")
    asyncio.create_task(embed_sqs_client.poll_sqs())  # Start polling SQS in the background

@app.get("/")
def read_root():
    return {"message": "Welcome to Embed Service API!"}