from typing import List

import spacy
import Stemmer
from rank_bm25 import BM25Okapi
from sqlmodel import Session, select
from tqdm import tqdm

from matching.database import models
from matching.models.search.main import SearchModel

nlp = spacy.load("ru_core_news_md")
stemmer = Stemmer.Stemmer('russian')


def _preprocess_documents(documents: List[str]) -> List[List[str]]:
    result = [
        stemmer.stemWords([token.lemma_ for token in document])
        for document in tqdm(nlp.pipe(documents, batch_size=64, n_process=16, disable=["parser", "ner"]))
    ]
    return result


class BM25SearchModel(SearchModel):
    def __init__(self, session: Session):
        products = session.exec(select(models.Product)).fetchall()
        self.product_ids = [i.item_id for i in products]
        names = [i.name for i in products]
        self.index = BM25Okapi(_preprocess_documents(names))

    def search(self, name: str, max_n: int, session: Session) -> List[models.Product]:
        query = stemmer.stemWords([token.lemma_ for token in nlp(name)])
        item_ids = self.index.get_top_n(query, self.product_ids, max_n)
        results = session.exec(select(models.Product).where(models.Product.item_id.in_(item_ids))).fetchall()
        return results
