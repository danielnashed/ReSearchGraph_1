from .crud import paperCRUD as CRUD
import json

async def create_embeddings(message):
    # Implement your message processing logic here
    print("Processing message:", message)
    # Get papers by user ID and collection ID
    body = json.loads(message["Body"].replace("'", '"'))
    papers = await CRUD.get_papers(body["user_id"], body["collection_id"])
    print("Papers:", papers)
    print("Embeddings created")
