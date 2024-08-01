from typing import Sequence

from flask import Blueprint, Flask, Response, request

from ..app.resources import Match
from ..utils.decorators import require_int
from .source import DataSource
from .response import ResponseFactory, Message


class GameBlueprint:
    """
    Takes in a `DataSource` subclass and creates all of the flask routes based on the data fetching functions implemented
    by the developer
    """

    def __init__(
        self, game: str, import_name: str, *sources: Sequence[DataSource]
    ) -> None:
        """
        Args:
            router (DataSource): Object containing all the overriden static methods for the endpoints
            game (str): The name of the game to create the blueprint for
            import_name (str): The import_name of the blueprint (should just be __name__ for 99% of use cases)
        """

        self.sources = sources
        self.game = game

        self._bp = Blueprint(self.game, import_name)
        self.url = f"/{self.game}"

        # Player endpoints
        self.create_endpoint(
            "/player/<player_id>", "get_player", "player_id", self.get_player
        )
        self.create_endpoint(
            "/player/<player_id>/matches",
            "get_player_matches",
            "player_id",
            self.get_player_matches,
        )
        self.create_endpoint(
            "/player/<player_id>/teams",
            "get_player_teams",
            "player_id",
            self.get_player_teams,
        )

        # Team endpoints
        self.create_endpoint("/team/<team_id>", "get_team", "team_id", self.get_team)
        self.create_endpoint(
            "/team/<team_id>/matches",
            "get_team_matches",
            "team_id",
            self.get_team_matches,
        )
        self.create_endpoint(
            "/team/<team_id>/players",
            "get_team_players",
            "team_id",
            self.get_team_players,
        )

        # Match endpoints
        self.create_endpoint(
            "/match/<match_id>", "get_match", "match_id", self.get_match
        )

        # Event methods
        self.create_endpoint(
            "/event/<event_id>", "get_event", "event_id", self.get_event
        )
        self.create_endpoint(
            "/event/<event_id>/matches",
            "get_event_matches",
            "event_id",
            self.get_event_matches,
        )
        self.create_endpoint(
            "/event/<event_id>/teams",
            "get_event_teams",
            "event_id",
            self.get_event_teams,
        )

    @staticmethod
    def require_implemented(
        sources: Sequence[DataSource], game: str, callback: str, endpoint: str
    ):
        """Enforce the function wrapped by this decorator to return `ResponseFactory.error` instance if the given
        `DataSource` does not implement the given callback method

        Args:
            callback (str): the name of the method that must be implemented by the `DataSource` for the decorated function to run
            endpoint (str): the name of the endpoint that this function is decorating
        """

        def require_implemented(func):
            def inner(*args, **kwargs):
                # Does one of our data sources implement the required callback
                if not any(DataSource.is_implemented(x, callback) for x in sources):
                    return ResponseFactory.error(
                        GameBlueprint._enpoint_unsupported_msg(game, endpoint)
                    )
                return func(*args, **kwargs)

            return inner

        return require_implemented

    def create_endpoint(
        self, endpoint: str, source_method: str, id_: str, func: callable
    ) -> None:
        """Create a standard endpoint that does three things:
            - Checks that the function required for the endpoint is implemented. If it is not, it returns an error `Response`
            - Casts the id parameter marked by `id_` to an integer. If it cannot be castm it returns an error `Response`
            - Registers the created endpoint with this classes blueprint

        Args:
            endpoint (str): The endpoint path.
            source_method (str): the name of the DataSource method this endpoint uses
            id_ (str): the id_ of the endpoint which will be cast to an integer
            func (callable): the function to call when the endpoint is visited
        """

        @GameBlueprint.reqire_implemented(
            self.sources, self.game, source_method, endpoint
        )
        def create_endpoint():
            @require_int(id_, Message.invalid_identifier_error(id_))
            def get_resource(*args, **kwargs):
                return func(*args, **kwargs)

            return get_resource

        self._bp.add_url_rule(endpoint, source_method, create_endpoint())

    def get_resource_fcf(self, res: str, *args, **kwargs):
        """Get the given resource using the first-come-first idiom, IE the first data source that returns a valid response
        is the one that is prioritised

        Args:
            res (str): The resource to get. getattr(source, get_res) will be the function called for each data source

        Returns:
            _type_: _description_
        """
        resources = filter(
            lambda x: x is not None and x != [],
            [getattr(f"get_{res}", res)(*args, **kwargs) for source in self.sources],
        )
        return next(resources)

    def get_player(self, player_id: int) -> Response:
        # Fetch the data
        player = self.get_resource_fcf("player", player_id)
        # Return the palyer data if it exists
        return ResponseFactory.conditional(
            player is not None,
            player.to_dict() if player else None,
            "This player does not exist",
        )

    def get_player_matches(self, player_id: int) -> Response:
        player_matches: list[Match] = self.get_resource_fcf(
            "player_matches", player_id, request.args.get("page", 1)
        )
        return ResponseFactory.conditional(
            player_matches is not None,
            [m.to_dict() for m in player_matches],
            "There was an incredible server error fuck off",
        )

    def get_player_teams(self, player_id: int) -> list[None]:
        player_teams = self.get_resource_fcf("player_teams", player_id)
        return ResponseFactory.conditional(
            player_teams, [team.to_dict() for team in player_teams]
        )

    def get_team(self, team_id: int):
        team = self.get_resource_fcf("team", team_id)
        return ResponseFactory.conditional(
            team,
            team.to_dict() if team else {},
            "No team with the given team_id could be found",
        )

    def get_team_matches(self, team_id: int):
        matches = self.get_resource_fcf(
            "team_matches", team_id, page=int(request.args.get("page", 1))
        )
        return ResponseFactory.conditional(
            matches,
            [m.to_dict() for m in matches],
            "No matches could be found for the given team",
        )

    def get_team_players(self, team_id):
        players = self.get_resource_fcf("team_players", team_id)
        return ResponseFactory.conditional(
            players,
            [p.to_dict() for p in players],
            "There were no players to be found",
        )

    def get_match(self, match_id: int):
        match = self.source.get_resource_fcf("match", match_id)
        return ResponseFactory.conditional(
            match,
            match.to_dict() if match else {},
            "There was no match to be found",
        )

    def get_event(self, event_id: int):
        event = self.get_resource_fcf("event", event_id)
        return ResponseFactory.conditional(
            event, event.to_dict() if event else {}, "No event could be found"
        )

    def get_event_matches(self, event_id: int):
        matches = self.get_resource_fcf("event_matches", event_id)
        return ResponseFactory.conditional(
            matches, [m.to_dict() for m in matches], "No matches to be found"
        )

    def get_event_teams(self, event_id: int):
        teams = self.get_resource_fcf("event_teams", event_id)
        return ResponseFactory.conditional(
            teams, [team.to_dict() for team in teams], "No teams found"
        )

    def register(self, app: Flask) -> None:
        """Registers this blueprint with the given app

        Args:
            app (Flask): Flask app to register the blueprint to
        """
        app.register_blueprint(self._bp, url_prefix=self.url)
