from typing import List

from matching.models.matching.main import MatchingModel
from matching.models.search.main import SearchModel
from matching.database import models


class SearchWrapper:
    def __init__(self, search_model: SearchModel,
                 matching_model: MatchingModel):
        self.search_model = search_model
        self.matching_model = matching_model

    def get_matches(self, product: models.Product) -> List[models.Product]:
        matched = self.matching_model.find(product)
        return matched

    def search(self, name: str, max_search_candidates: int) -> List[List[models.Product]]:
        search_results = self.search_model.search(name, max_search_candidates)
        results = []
        seen_products = set()
        for product in search_results:
            if product in seen_products:
                continue
            matched = self.get_matches(product)
            product_group = [product, *matched]
            results.append(product_group)
            seen_products.update(product_group)
        return results
