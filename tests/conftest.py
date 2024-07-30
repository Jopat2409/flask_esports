import pytest

from flask_esports.config import set_testing
from flask_esports.app import create_app

@pytest.fixture()
def app():
    set_testing(True)
    app = create_app()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
