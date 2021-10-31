from typing import List

from fastapi import FastAPI, Query, Depends
# noinspection PyUnresolvedReferences
from sqlmodel import Session, select

from matching.database import models
from matching.database.main import create_db_and_tables, engine

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/search", response_model=List[List[models.Product]])
def search(
        name: str = Query(..., description="String to search in product name"),
        max_n: int = Query(..., description="Max number of results"),
        session: Session = Depends(get_session),
):
    return [[session.exec(select(models.Product).limit(1)).one(), ], ]


@app.get("/matches", response_model=List[models.Product])
def get_matches(
        product_id: int = Query(..., description="Product id to get matches for"),
        session: Session = Depends(get_session),
):
    return [session.exec(select(models.Product).limit(1)).one(), ]
