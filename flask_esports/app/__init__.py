import os
from flask import Flask
from importlib import import_module

from ..config import Config

def register_game(app: Flask, game: str) -> None:
    """Registers a game's API endpoint with the main app

    Args:
        app (Flask): the `Flask` app to register the game API with
        game (str): The name of the game to register (IE the name of the folder that routes.py is in)
    """
    module = Config.API_ENDPOINT_DIR.replace('\\', '/').replace('/', '.')
    router = getattr(import_module(f"{module}.{game}"), "router")
    router.register(app)

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # We need the app context because if a route is not implemented it defaults to a jsonified error message
    with app.app_context():
        # Loop through each endpoint directory and register the respective API routers
        for route in os.listdir(os.path.join(Config.BASE_DIRECTORY, Config.API_ENDPOINT_DIR)):
            register_game(app, route)

    return app
