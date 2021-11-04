from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session

from matching.database import models


class SearchModel(ABC):
    @abstractmethod
    def search(self, name: str, max_n: int, session: Session) -> List[models.Product]:
        raise NotImplementedError()
