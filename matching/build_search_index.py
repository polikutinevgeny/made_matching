from pathlib import Path

from sqlmodel import Session

from matching.database.main import engine
from matching.models.search.bm25 import BM25SearchModel
from matching.env import BM25_PATH


if __name__ == '__main__':
    path = Path(BM25_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with Session(engine) as session:
        index = BM25SearchModel(session)
        index.save(path)
