from abc import ABC, abstractmethod
from typing import List

from matching.database import models


class MatchingModel(ABC):
    @abstractmethod
    def find(self, product: models.Product) -> List[models.Product]:
        raise NotImplementedError()
