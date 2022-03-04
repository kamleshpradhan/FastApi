from fastapi.testclient import TestClient
import py
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,engine
from app import models
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:123456789@localhost:5432/fastapi_testing"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # when using sql database we have add this to above, connect_args={"check_same_thread": False}
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# from alembic import command
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# _test to pull from env 


# {settings.database_url}

# models.Base.metadata.create_all(bind=engine)
# Base = declarative_base()
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)


@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
         yield db
    finally:
        db.close()





@pytest.fixture()
def client(session):
    # run our code before we yeild run our test run our code after our test finishes
    # models.Base.metadata.drop_all(bind=engine)
    # models.Base.metadata.create_all(bind=engine)
    # using alembic
    # command.upgrade("head")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # command.downgrade("head")
    