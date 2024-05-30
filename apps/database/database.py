import os
from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(url=DATABASE_URL, echo=False, future=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def init_db() -> None:
    SQLModel.metadata.create_all(bind=engine)
