from esports_api.utils.game_router import GameBlueprint
from esports_api.app.tf2.routes import Tf2Routes

router = GameBlueprint(Tf2Routes, "tf2", __name__)
