import pytest
from sqlalchemy import create_engine

from http_server import tables


@pytest.fixture(scope='session')
def engine():
    return create_engine('postgresql://localhost/test_database')

@pytest.yield_fixture(scope='session')
def create_tables(engine):
    tables.metadata.create_all(engine)
    yield
    tables.metadata.drop_all(engine)