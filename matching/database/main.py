from sqlmodel import create_engine, SQLModel

from matching.env import DATABASE_URL

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
