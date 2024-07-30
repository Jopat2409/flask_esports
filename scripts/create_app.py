"""This script is made to streamline the process of setting up an API application using the flask_esports package

It will create a project that uses the following template
    root
    |- api
        |- endpoints
            |- game1
                |- __init__.py
                |- routes.py
            |- game2
                |- __init__.py
                |- routes.py
                |- constants.py
        |- main.py
    |- venv
    |- tests
    |- README etc.

Where each game (endpoint) that will be implemented into the project is specified as a CL argument.

Each router.py file subclasses the `GameRouter` class to implement methods for fetching data from whatever source
is being used.

Each __init__.py file imports this subclassed `GameRouter` and creates a `GameBlueprint` with it, whichr registers
all the correct routes with the central flask application
"""

import os
import sys


def create_route_file(root: str, endpoint: str) -> None:
    """
    Creates a default router file for a specific API endpoint.

    Contains am implementation of the GameRouter class which implements each function required for fetching resources
    from the given data point.
    """
    with open(os.path.join(root, "router.py"), "w+", encoding="utf-8") as f:
        f.write(f"""from esports_api.app.game_router import GameRouter
from esports_api.app.response_factory import ResponseFactory

from esports_api.app.resources import Player, Match, Team, Event

class {endpoint.lower().capitalize()}Router(GameRouter):

    def get_player(player_id: int) -> Player | None:
        return None

    @staticmethod
    def get_player_matches(player_id: int, page: int) -> list[Match]:
        return None

    @staticmethod
    def get_player_teams(player_id: int) -> list[Team]:
        return None

    @staticmethod
    def get_team(team_id: int) -> Team | None:
        return ResponseFactory.error("This game does not support getting team data")

    @staticmethod
    def get_team_matches(team_id: int, page: int) -> list[Match]:
        return ResponseFactory.error("This game does not support getting a team's matches")

    @staticmethod
    def get_team_players(team_id: int) -> list[Player]:
        return ResponseFactory.error("This game does not support getting a team's previous rosters")

    @staticmethod
    def get_match(match_id: int) -> Match:
        return ResponseFactory.error("This game does not support getting match data")

    @staticmethod
    def get_event(event_id: int) -> Event:
        return ResponseFactory.error("This game does not support events")

    @staticmethod
    def get_event_matches(event_id: int) -> list[Match]:
        return ResponseFactory.error("This game does not support getting matches by event")

    @staticmethod
    def get_event_teams(event_id: int) -> list[Team]:
        return ResponseFactory.error("This game does not support getting the teams from an event")""")


def create_init_file(root: str, endpoint: str) -> None:
    with open(os.path.join(root, "__init__.py"), "w+", encoding="utf-8") as f:
        f.write(f"""from esports_api.app.game_blueprint import GameBlueprint
from endpoints.{endpoint}.router import {endpoint.lower().capitalize()}Router

router = GameBlueprint({endpoint.lower().capitalize()}Router, "{endpoint}", __name__)""")


def create_tree(root: str, tree: dict) -> None:
    """Creates a directory tree given a dictionary representing the directory tree to create.

    For example, `{'tests': {}, 'src': {}}` would create two empty directories `root/tests` and `root/utils`,
    wheras `{'tests': {'utils': {}, 'endpoints': {}}}` would create `root/tests`, `root/tests/utils` and `root/tests/endpoints`

    Args:
        root (str): The root folder to create the directory tree from
        tree (dict): The tree, given as a dictionary where each key represents a directory name, and the dict value its directory contents

    Returns:
        None
    """
    for branch in tree:
        os.mkdir(os.path.join(root, branch))
        create_tree(os.path.join(root, branch), tree[branch])


def setup_project_structure(root: str, endpoints: list[str]):
    """Project directory should look something like"""
    create_tree(
        root,
        {
            "api": {
                "endpoints": {ep: {} for ep in endpoints},
                "helpers": {},
            },
            "tests": {},
        },
    )


def create_app(endpoints):
    root_dir = os.getcwd()
    setup_project_structure(root_dir, endpoints)
    for endpoint in endpoints:
        create_route_file(
            os.path.join(root_dir, "api", "endpoints", endpoint), endpoint
        )
        create_init_file(os.path.join(root_dir, "api", "endpoints", endpoint), endpoint)


if __name__ == "__main__":
    args = sys.argv
    create_app(args[1:])
