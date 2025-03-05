from fastapi import FastAPI
from .routes import users
from .middleware import setup_middleware
from .db import init as init_db
from requests.exceptions import RequestException
from .aws.sqs_client import SQSClient
from .utils import create_clusters
from dotenv import load_dotenv
import asyncio
import os

# insert comment to test CI/CD pipelineee

load_dotenv()

app = FastAPI(title="Cluster Service API")

setup_middleware(app)
app.include_router(users.router)

# Initialize the SQS client for output queue
graph_queue_url = os.getenv('AWS_SQS_GRAPH_URL')
graph_sqs_client = SQSClient(graph_queue_url)

# Initialize the SQS client for input queue
cluster_queue_url = os.getenv('AWS_SQS_CLUSTER_URL')
cluster_sqs_client = SQSClient(cluster_queue_url, 
                             process_message=create_clusters, 
                             consumer=graph_sqs_client
                             )

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie
    print("Database connected")
    asyncio.create_task(cluster_sqs_client.poll_sqs())  # Start polling SQS in the background

@app.get("/")
def read_root():
    return {"message": "Welcome to Cluster Service API!"}