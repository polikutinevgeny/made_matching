from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
N_PROCESS = int(getenv("N_PROCESS", "1"))
ENVIRONMENT = getenv("ENVIRONMENT", "PRODUCTION")
BM25_PATH = getenv("BM25_PATH", "cache/bm25.pickle")
