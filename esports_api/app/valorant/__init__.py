from esports_api.utils.game_router import GameBlueprint
from esports_api.app.valorant.routes import ValorantRoutes

router = GameBlueprint(ValorantRoutes, "valorant", __name__)
