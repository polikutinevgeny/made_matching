from typing import List, Dict
import logging

from fastapi import FastAPI, Query, Depends
# noinspection PyUnresolvedReferences
from sqlmodel import Session, select
from pydantic import conint
from fastapi.middleware.cors import CORSMiddleware

from matching.database import models
from matching.database.main import create_db_and_tables, engine
from matching.models.matching.main import MatchingModel
from matching.models.search.bm25 import BM25SearchModel
from matching.env import ENVIRONMENT, BM25_PATH
from matching.models.matching.file import FileMatchingModel
from matching.schemas import MODEL_MAPPING, MatchingModelType

# if ENVIRONMENT == "PRODUCTION":
#     from matching.models.matching.stub import StubMatchingModel as MatchingModel
# elif ENVIRONMENT == "DEV":
#     from matching.models.matching.fasttext import FasttextMatchingModel as MatchingModel
# else:
#     raise RuntimeError()

app = FastAPI()
search_model: BM25SearchModel
model_dict: Dict[MatchingModelType, MatchingModel] = {name: FileMatchingModel(path) for name, path in MODEL_MAPPING.items()}

logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    global search_model
    global models
    # create_db_and_tables()
    with Session(engine) as session:
        logger.info("Loading search index...")
        search_model = BM25SearchModel.load(BM25_PATH)
        logger.info("Search index loaded successfully")
        # logger.info("Loading matching model...")
        # matching_model = MatchingModel(session)
        # logger.info("Matching model loaded successfully")


@app.get("/search", response_model=List[List[models.Product]])
def search(
        name: str = Query(..., description="String to search in product name"),
        max_n: conint(le=100) = Query(..., description="Max number of results"),
        session: Session = Depends(get_session),
        model_type: MatchingModelType = Query(default=MatchingModelType.BASELINE)
):
    search_results = search_model.search(name, max_n, session)
    all_results = model_dict[model_type].find(search_results, session)
    return all_results
