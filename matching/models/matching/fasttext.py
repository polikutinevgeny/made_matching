from typing import List, Union

import faiss
import numpy as np
import spacy
from gensim.models import fasttext
from sqlmodel import Session, select
from tqdm import tqdm

from matching.database import models
from matching.models.matching.main import MatchingModel

nlp = spacy.load("ru_core_news_md")
ft = fasttext.load_facebook_vectors("ft_native_300_ru_wiki_lenta_lemmatize.bin")


def _build_vectors(documents: List[str], n_process=1) -> np.ndarray:
    result = np.stack(
        [np.mean([ft[token.lemma_] for token in document], axis=0)
         for document in tqdm(nlp.pipe(documents, batch_size=64, n_process=n_process, disable=["parser", "ner"]))]
    )
    return result


class FasttextMatchingModel(MatchingModel):
    def __init__(self, session: Session):
        products = session.exec(select(models.Product)).fetchall()
        self.product_ids = np.array([i.item_id for i in products])
        self.product_idx = np.arange(len(self.product_ids)).astype(np.int64)
        names = [i.name for i in products]
        self.vectors = _build_vectors(names, n_process=16)
        faiss.normalize_L2(self.vectors)
        self.index = faiss.index_factory(self.vectors.shape[1], "IDMap,Flat")
        self.index.add_with_ids(self.vectors, self.product_idx)

    def find(
            self,
            products: Union[models.Product, List[models.Product]],
            session: Session
    ) -> List[List[models.Product]]:
        if not isinstance(products, list):
            products = [products, ]
        query = _build_vectors([i.name for i in products])
        faiss.normalize_L2(query)
        scores, found = self.index.search(query, 10)
        found_product_ids = self.product_ids[found.flatten()]
        found_products = {i.item_id: i for i in session.exec(
            select(models.Product).where(
                models.Product.item_id.in_(found_product_ids.tolist()))).fetchall()}
        result = []
        for group, group_scores in zip(found, scores):
            product_ids = self.product_ids[group]
            chains = set()
            selected_products = []
            for product_id, score in zip(product_ids, group_scores):
                product = found_products[product_id]
                if product.chain_id not in chains:
                    chains.add(product.chain_id)
                    selected_products.append(product)
            result.append(selected_products)
        return result
