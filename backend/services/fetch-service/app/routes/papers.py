from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import arxiv
import datetime
import uuid
from pydantic import BaseModel
from ..crud import paperCRUD as CRUD
from ..aws.sqs_client import SQSClient

router = APIRouter(prefix="/fetch-papers", tags=["Papers"])

class paperRequest(BaseModel):
    user_id: str

# Fetch papers from external source
@router.post("/")
async def create_papers_route(request: paperRequest):

    # ID unique to each batch of papers fetched together
    collection_id = str(uuid.uuid4())[:8]

    # Get current date and time in GMT
    now = datetime.datetime.now(datetime.timezone.utc)
    yesterday = (now - datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')

    # Format the date range
    date_range = f"[{yesterday} TO {now.strftime('%Y%m%d%H%M')}]"

    # # Only retrieve papers from yesterday to today
    # yesterday = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime('%Y%m%d')
    
    # Primary categories to search for
    categories = ["cs.AI", "cs.AR", "cs.CL", "cs.CV", "cs.GL", "cs.LG", "cs.MA", "cs.NE", "cs.RO"]
    # Build query string
    query = " OR ".join([f"cat:{category}" for category in categories])
    # query += f" AND submittedDate:[{yesterday} TO *]"
    query += f" AND submittedDate:{date_range}"
    print("Query:", query)

    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for result in search.results():
        print(result)
        papers.append({
            "collection_id": collection_id,
            "user_id": request.user_id,
            "arxiv_id": result.get_short_id(),
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "abstract": result.summary,
            "published": result.published.isoformat() if hasattr(result.published, 'isoformat') else result.published,
            "category": result.primary_category,
            "url": result.entry_id,
            "pdf_url": result.pdf_url
        })
    
    # Create a new paper in the database
    for paper in papers:
        await CRUD.create_paper(paper)

    # Create queue message 
    message = {
        "collection_id": collection_id,
        "user_id": request.user_id,
        "papers_count": len(papers),
        "timestamp": now.isoformat()
    }

    # Inject message to queue
    sqs_client = SQSClient()
    await sqs_client.send_message(message)

    
    return JSONResponse(content={"papers": papers}, 
                        status_code=201)
