from typing import Union, List

from sqlmodel import Session, select

from matching.database import models
from matching.models.matching.main import MatchingModel


class StubMatchingModel(MatchingModel):
    def __init__(self, *args, **kwargs):
        pass

    def find(
            self,
            products: Union[models.Product, List[models.Product]],
            session: Session
    ) -> List[List[models.Product]]:
        if not isinstance(products, list):
            products = [products, ]
        return [[product] * 2 for product in products]
