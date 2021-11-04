from abc import ABC, abstractmethod
from typing import List, Union

from sqlmodel import Session

from matching.database import models


class MatchingModel(ABC):
    @abstractmethod
    def find(self, product: Union[models.Product, List[models.Product]], session: Session) -> List[models.Product]:
        raise NotImplementedError()
