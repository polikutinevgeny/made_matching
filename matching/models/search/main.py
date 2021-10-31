from abc import ABC, abstractmethod
from typing import List

from matching.database import models


class SearchModel(ABC):
    @abstractmethod
    def search(self, name: str, max_n: int) -> List[models.Product]:
        raise NotImplementedError()
