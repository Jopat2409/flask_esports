import requests

from esports_api.utils.decorators import require_int
from esports_api.utils.game_router import GameRouter
from esports_api.utils.response_factory import ResponseFactory
from esports_api.app.models.player import SourceId, Player


class Tf2Routes(GameRouter):

    def get_player(player_id):

        response = requests.get(f"https://api.rgl.gg/v0/profile/{player_id}")
        rgl_data = response.json()
        player = Player(
            SourceId("tf2_rgl", player_id),
            rgl_data.get("name", None),
            rgl_data.get("forename", None),
            rgl_data.get("surname", None),
            rgl_data.get("avatar", None),
            rgl_data.get("currentTeams", {})["sixes"]["id"]
        )

        return player

    def get_player_teams(player_id: str):

        return ResponseFactory.success([{"name": "froyotech", "tag": "FROYO", "id": 1234, "joined-at": 0.0, "left-at": 0.0}, {"name": "High roller gaming", "tag": "4k", "id": 1, "joined-at": 0.0, "left-at": 0.0}])

    def get_player_rosters(player_id: str):

        return []

    def get_player_matches(player_id: int):
        return []

