from typing import Generator

import pytest
from fastapi.testclient import TestClient

from apps.database import database
from sqlmodel import Session
from apps.main import app

import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[database.get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
