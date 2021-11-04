from typing import List
import logging

from fastapi import FastAPI, Query, Depends
# noinspection PyUnresolvedReferences
from sqlmodel import Session, select

from matching.database import models
from matching.database.main import create_db_and_tables, engine
from matching.models.matching.fasttext import FasttextMatchingModel
from matching.models.search.bm25 import BM25SearchModel

app = FastAPI()
search_model: BM25SearchModel
matching_model: FasttextMatchingModel

logger = logging.getLogger("uvicorn")


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    global search_model
    global matching_model
    create_db_and_tables()
    with Session(engine) as session:
        logger.info("Loading search index...")
        search_model = BM25SearchModel(session)
        logger.info("Search index loaded successfully")
        logger.info("Loading matching model...")
        matching_model = FasttextMatchingModel(session)
        logger.info("Matching model loaded successfully")


@app.get("/search", response_model=List[List[models.Product]])
def search(
        name: str = Query(..., description="String to search in product name"),
        max_n: int = Query(..., description="Max number of results"),
        session: Session = Depends(get_session),
):
    search_results = search_model.search(name, max_n, session)
    all_results = matching_model.find(search_results, session)
    return all_results


@app.get("/matches", response_model=List[models.Product])
def get_matches(
        product_id: int = Query(..., description="Product id to get matches for"),
        session: Session = Depends(get_session),
):
    return [session.exec(select(models.Product).limit(1)).one(), ]
