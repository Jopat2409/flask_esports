import pytest

from flask_esports.api.blueprint import GameBlueprint


def test_get_player():
    test_blueprint = GameBlueprint()