from .crud import paperCRUD as CRUD
from .aws.bedrock_client import BedrockClient
import json

async def create_embeddings(message):
    print("Processing message:", message)
    # Get papers by user ID and collection ID
    body = json.loads(message["Body"].replace("'", '"'))
    papers = await CRUD.get_papers(body["user_id"], body["collection_id"])
    # Build request body for embedding service
    text = [paper.title + ": " + paper.abstract for paper in papers]
    embedding_model = BedrockClient(model_id='cohere.embed-english-v3')
    # Create embeddings
    response = embedding_model.invoke_model(json.dumps({
                                            "texts": text,
                                            "input_type": "search_document"
                                            }
                                        ))
    # Save embeddings to database
    for embedding, paper in zip(response["embeddings"], papers):
        paper.summary_embedding = embedding
        await paper.save()

    # Update papers with embeddings
    print("Embeddings created")

    return {"message": "Embeddings created"}

