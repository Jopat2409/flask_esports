from flask_esports.api.game_router import GameBlueprint, GameRouter

class TestRouter(GameRouter):

    def get_player(player_id: int) -> None:
        return None

def test_require_implemented(app):

    assert GameRouter.is_implemented(TestRouter, "get_player")
    assert not GameRouter.is_implemented(TestRouter, "get_team")

    @GameBlueprint.require_implemented("get_player", "/player")
    def test_require_implemented(game: str, router: GameRouter):
        return "Test Solution"

    assert test_require_implemented("tf2", TestRouter) == "Test Solution"

    @GameBlueprint.require_implemented("get_player", "/player")
    def test_require_implemented(game: str, router: GameRouter):
        return "Test Solution"

    assert test_require_implemented(game="tf2", router=TestRouter) == "Test Solution"

    @GameBlueprint.require_implemented("get_team", "/team")
    def test_require_implemented(game: str, router: GameRouter):
        return "Test Solution"
    with app.app_context():
        assert test_require_implemented("tf2", TestRouter).get_json()["success"] is False
    @GameBlueprint.require_implemented("get_team", "/team")
    def test_require_implemented(game: str, router: GameRouter):
        return "Test Solution"

    with app.app_context():
        assert test_require_implemented(game="tf2", router=TestRouter).get_json()["success"] is False
