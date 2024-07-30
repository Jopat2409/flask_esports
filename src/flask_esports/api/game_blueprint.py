from flask import Blueprint, Flask, Response, request


from .game_router import GameRouter
from .response_factory import ResponseFactory

from ..app.resources import Player, Match
from ..app.db.query_factory import BasicQuery, insert_one

from ..utils.decorators import require_int

class GameBlueprint:
    """
    Takes in a `GameRouter` subclass and registers all of the static functions to the correct routes
    """

    @staticmethod
    def require_implemented(callback: str, endpoint: str):
        """Decorator that forces a function to return a `ResponseFactory.error` instance if the given `GameRouter`
        does not implement the given callback method

        Args:
            callback (str): the name of the method that must be implemented for the decorated function to run
            endpoint (str): the name of the endpoint that this function is decorating
        """
        def require_implemented(func):
            def inner(*args, **kwargs):
                game = kwargs.get("game", None) or args[0]
                router = kwargs.get("router", None) or args[1]
                if not GameRouter.is_implemented(router, callback):
                    return ResponseFactory.error(GameBlueprint._enpoint_unsupported_msg(game, endpoint))
                return func(*args, **kwargs)
            return inner
        return require_implemented

    @staticmethod
    def _enpoint_unsupported_msg(game: str, endpoint: str) -> str:
        """Creates an unsupported endpoint error message indicating that the API does not have support for the given endpoint

        Args:
            game (str): The game that the endpoint is attempting to be reached on (/tf2, /valorant etc.)
            endpoint (str): the endpoint

        Returns:
            str: the error message
        """
        return f"The {game} API does not support {endpoint}. Please refer to the documentation for a list of available endpoints."

    @staticmethod
    def _invalid_id_msg(id_: str) -> str:
        """Creates an error message indicating that the given ID was invalid

        Args:
            id_ (str): the name of the id parameter that was invalid

        Returns:
            str: the error message
        """
        return f"The given value of {id_} is invalid. It must be an integer value."

    @require_implemented("get_player", "/player")
    def create_get_player_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("player_id", "The player ID must be a valid integer")
        def get_player(player_id: int) -> Response:

            # Get the player from the database
            db_player= BasicQuery(Player, game, player_id=player_id).execute(one=True)

            # Return the data if it exists in the database
            if db_player:
                return ResponseFactory.success(db_player.to_dict())

            # Fetch the data and insert into database
            player = router.get_player(player_id)
            if player is not None:
                insert_one(player)

            # Return the palyer data if it exists
            return ResponseFactory.conditional(player is not None, player.to_dict() if player else None, "This player does not exist")

        return get_player

    @require_implemented("get_player_matches", "/player/matches")
    def create_get_player_matches_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("player_id", "The player ID must be a valid integer")
        def get_player_matches(player_id: int) -> Response:

            player_matches: list[Match] = router.get_player_matches(player_id, request.args.get("page", 1))
            return ResponseFactory.conditional(player_matches is not None, [m.to_dict() for m in player_matches], "There was an incredible server error fuck off")

        return get_player_matches

    @require_implemented("get_player_teams", "/player/teams")
    def create_get_player_teams_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("player_id", GameBlueprint._invalid_id_msg("player_id"))
        def get_player_teams(player_id: int) -> list[None]:

            player_teams = router.get_player_teams(player_id)
            return ResponseFactory.conditional(player_teams, [team.to_dict() for team in player_teams])

        return get_player_teams

    @require_implemented("get_team", "/team")
    def create_get_team_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("team_id", GameBlueprint._invalid_id_msg("team_id"))
        def get_team(team_id: int):
            team = router.get_team(team_id)
            return ResponseFactory.conditional(team, team.to_dict() if team else {}, "No team with the given team_id could be found")
        return get_team

    @require_implemented("get_team_matches", "/team/matches")
    def create_get_team_matches_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("team_id", GameBlueprint._invalid_id_msg("team_id"))
        def get_team_matches(team_id: int):
            matches = router.get_team_matches(team_id, page=int(request.args.get("page", 1)))
            return ResponseFactory.conditional(matches, [m.to_dict() for m in matches], "No matches could be found for the given team")
        return get_team_matches

    @require_implemented("get_team_players", "team/players")
    def create_get_team_players_endpoint(game: str, router: GameRouter, current: bool) -> callable:

        @require_int("team_id", GameBlueprint._invalid_id_msg("team_id"))
        def get_team_players(team_id):
            players = router.get_team_players(team_id)
            if current:
                # Filter for only current players
                pass
            return ResponseFactory.conditional(players, [p.to_dict() for p in players], "There were no players to be found")
        return get_team_players

    @require_implemented("get_match", "/match")
    def create_get_match_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("match_id", GameBlueprint._invalid_id_msg("match_id"))
        def get_match(match_id: int):
            match = router.get_match(match_id)
            return ResponseFactory.conditional(match, match.to_dict() if match else {}, "There was no match to be found")
        return get_match

    @require_implemented("get_event", "/event")
    def create_get_event_endpoint(game: str, router: GameRouter) -> callable:

        @require_int("event_id", GameBlueprint._invalid_id_msg("event_id"))
        def get_event(event_id: int):
            event = router.get_event(event_id)
            return ResponseFactory.conditional(event, event.to_dict() if event else {}, "No event could be found")
        return get_event

    @require_implemented("get_event_matches", "/event/matches")
    def create_get_event_matches_endpoint(game: str, router: GameRouter):

        @require_int("event_id", GameBlueprint._invalid_id_msg("event_id"))
        def get_event_matches(event_id: int):
            matches = router.get_event_matches(event_id)
            return ResponseFactory.conditional(matches, [m.to_dict() for m in matches], "No matches to be found")
        return get_event_matches

    @require_implemented("get_event_teams", "/event/teams")
    def create_get_event_teams_endpoint(game: str, router: GameRouter):

        @require_int("event_id", GameBlueprint._invalid_id_msg("event_id"))
        def get_event_teams(event_id: int):
            teams = router.get_event_teams(event_id)
            return ResponseFactory.conditional(teams, [team.to_dict() for team in teams], "No teams found")
        return get_event_teams

    def __init__(self, router: GameRouter, game: str, import_name: str):
        """
        Args:
            router (GameRouter): Object containing all the overriden static methods for the endpoints
            game (str): The name of the game to create the blueprint for
            import_name (str): The import_name of the blueprint (should just be __name__ for 99% of use cases)
        """
        self._bp = Blueprint(game, import_name)
        self.url = f"/{game}"

        # Player methods
        self._bp.add_url_rule("/player/<player_id>", "get_player", GameBlueprint.create_get_player_endpoint(game, router))
        self._bp.add_url_rule("/player/<player_id>/matches", "get_player_matches", GameBlueprint.create_get_player_matches_endpoint(game, router))
        self._bp.add_url_rule("/player/<player_id>/teams", "get_player_teams", GameBlueprint.create_get_player_teams_endpoint(game, router))

        # Team methods
        self._bp.add_url_rule("/team/<team_id>", "get_team", GameBlueprint.create_get_team_endpoint(game, router))
        self._bp.add_url_rule("/team/<team_id>/matches", "get_team_matches", GameBlueprint.create_get_team_matches_endpoint(game, router))
        self._bp.add_url_rule("/team/<team_id>/players", "get_team_players", GameBlueprint.create_get_team_players_endpoint(game, router, current=False))
        self._bp.add_url_rule("/team/<team_id>/players/current", "get_team_players_current", GameBlueprint.create_get_team_players_endpoint(game, router, current=True))

        # Match methods
        self._bp.add_url_rule("/match/<match_id>", "get_match", GameBlueprint.create_get_match_endpoint(game, router))

        # Event methods
        self._bp.add_url_rule("/event/<event_id>", "get_event", GameBlueprint.create_get_event_endpoint(game, router))
        self._bp.add_url_rule("/event/<event_id>/matches", "get_event_matches", GameBlueprint.create_get_event_matches_endpoint(game, router))
        self._bp.add_url_rule("/event/<event_id>/teams", "get_event_teams", GameBlueprint.create_get_event_teams_endpoint(game, router))

    def register(self, app: Flask) -> None:
        """Registers this blueprint with the given app

        Args:
            app (Flask): Flask app to register the blueprint to
        """
        app.register_blueprint(self._bp, url_prefix=self.url)
