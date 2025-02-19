from .crud import UserCRUD
from .crud import paperCRUD
from .crud import clusterCRUD
from .aws.bedrock_client import BedrockClient
from incdbscan import IncrementalDBSCAN
import json
import pickle

async def create_clusters(message):
    print("Processing message:", message) 
    # Get papers by user ID and collection ID
    body = json.loads(message["Body"].replace("'", '"'))
    user_id = body["user_id"]
    papers = await paperCRUD.get_papers(user_id, body["collection_id"])
    # Get user
    user = await UserCRUD.get_user_by_id(user_id)
    # Get user's clusterer
    clusterer = user.clusterer
    # Get embeddings for new collection of papers
    embeddings = [paper.summary_embedding for paper in papers]
    # Update clusterer with new embeddings
    clusterer.insert(embeddings)
    # Get cluster IDs for this paper collection
    cluster_ids = clusterer.get_cluster_labels(embeddings)
    # Create hash map of cluster IDs and papers
    hash_map = {cluster_id: [] for cluster_id in set(cluster_ids)}
    for cluster_id, paper in zip(cluster_ids, papers):
        hash_map[cluster_id].append(paper)
    # Get existing clusters from database 
    existing_clusters = await clusterCRUD.get_all_clusters(user_id)
    existing_cluster_ids = [cluster.cluster_id for cluster in existing_clusters]
    # Add papers to existing clusters or in new clusters
    for cluster_id, papers_in_cluster in hash_map.items():
        # Create cluster summary
        paper_summaries = '.\n\n'.join([paper.title + ": " + paper.abstract for paper in papers_in_cluster])
        summarization_model = BedrockClient(model_id='us.meta.llama3-2-11b-instruct-v1:0')
        formatted_prompt = format_prompt(paper_summaries)
        response = summarization_model.invoke_model(json.dumps({
                                                "prompt": formatted_prompt,
                                                "max_gen_len": 2048,
                                                "temperature": 0.5,
                                                }))
        print(response["generation"])
        print('\n\n\n')
        print(type(response["generation"]))
        response = json.loads(response["generation"])
        cluster_label, cluster_summary = response["cluster_label"], response["cluster_summary"]
        embedding_model = BedrockClient(model_id='cohere.embed-english-v3')
        # Create embedding for cluster summary
        response = embedding_model.invoke_model(json.dumps({
                                                "texts": [f"{cluster_label}: {cluster_summary}"],
                                                "input_type": "search_document"
                                                }))
        cluster_summary_embedding = response["embeddings"]
        # Build cluster dict 
        cluster_dict = {
            "cluster_id": cluster_id,
            "user_id": user_id,
            "label": cluster_label,
            "summary": cluster_summary,
            "summary_embedding": cluster_summary_embedding,
            "papers": [{"id": str(paper.id), "title": paper.title, "url": paper.pdf_url} for paper in papers_in_cluster]
        }
        if cluster_id in existing_cluster_ids:
            await clusterCRUD.update_cluster(cluster_dict)
        else:
            await clusterCRUD.create_cluster(cluster_dict)
    # Update user's clusterer
    user.clusterer = pickle.dumps(clusterer)
    await user.save()

    # Update papers with embeddings
    print("Clusters updated")
    return {"message": "Clusters updated"}


def format_prompt(user_msg: str) -> str:
    # Embed the prompt in Llama 3's instruction format.
    formatted_prompt = f"""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>

    You are an AI assistant tasked with taking a collection of research papers with title + abstracts and 
    generating a label and a summary. 
    1. The label must be short and relavent to the collection of papers. For example "LLM Quantization Methods". The label must be very specific to the subfield within the broader field of AI. 
    2. The summary must be a coherent but detailed summary of the collection of papers. 

    Please respond with a JSON object in the following format:
    {{
    "cluster_label": "text",
    "cluster_summary": "text"
    }}
    <|eot_id|><|start_header_id|>user<|end_header_id|>

    {user_msg}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    return formatted_prompt


