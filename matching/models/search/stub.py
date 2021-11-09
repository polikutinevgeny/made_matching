from typing import List

from sqlmodel import Session, select

from matching.database import models
from matching.models.search.main import SearchModel


class StubSearchModel(SearchModel):
    def __init__(self, *args, **kwargs):
        pass

    def search(self, name: str, max_n: int, session: Session) -> List[models.Product]:
        results = session.exec(
            select(models.Product).where(models.Product.name.ilike(f"%{name}%")).limit(10)).fetchall()
        return results
