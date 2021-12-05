from collections import defaultdict
from pathlib import Path
from typing import Union, List, Dict
from csv import DictReader

from sqlmodel import Session, select

from matching.database import models
from matching.models.matching.main import MatchingModel


class FileMatchingModel(MatchingModel):
    def __init__(self, file_path: Union[Path, str]):
        self.mapping: Dict[str, List[str]] = defaultdict(list)
        with open(file_path) as f:
            reader = DictReader(f)
            for row in reader:
                l = row["item_id_x"]
                r = row["item_id_y"]
                self.mapping[l].append(r)
                self.mapping[r].append(l)

    def _find_single(self, product: models.Product, session: Session) -> List[models.Product]:
        found = self.mapping[product.item_id]
        found_products = [i for i in session.exec(
            select(models.Product).where(
                models.Product.item_id.in_(found))).fetchall()]
        found_products.append(product)
        return found_products

    def find(
            self,
            products: Union[models.Product, List[models.Product]],
            session: Session
    ) -> List[List[models.Product]]:
        if not isinstance(products, list):
            products = [products, ]
        return [self._find_single(product, session) for product in products]
