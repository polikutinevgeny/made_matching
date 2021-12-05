from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
N_PROCESS = int(getenv("N_PROCESS", "1"))
ENVIRONMENT = getenv("ENVIRONMENT", "PRODUCTION")
BM25_PATH = Path(getenv("BM25_PATH", "cache/bm25.pickle"))
MODEL_FILE_PATH = Path(getenv("MODEL_FILE_PATH", "match_files"))
