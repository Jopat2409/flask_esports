import pytest

from esports_api import set_testing
from esports_api.app import create_app

@pytest.fixture()
def app():
    set_testing(True)
    app = create_app()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
