from flask import Flask
from importlib import import_module

from esports_api.config import Config
from esports_api.app.db.db import regenerate_db

def register_game(app: Flask, game: str):
    """Registers a game's API endpoint with the main app

    Args:
        app (Flask): the `Flask` app to register the game API with
        game (str): _description_
    """
    router = getattr(import_module(f"api.app.{game}"), "router")
    router.register(app)

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        register_game(app, "tf2")
        register_game(app, "valorant")

    # Completely public regenerate database url :DDD
    app.add_url_rule("/create-db", "create_db", regenerate_db)

    return app
