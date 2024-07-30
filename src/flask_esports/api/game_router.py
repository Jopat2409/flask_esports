"""Custom classes used to make implementing new games to the API a much easier ordeal

The `GameRouter` class contains all the static methods that should can be overridden to create your own API endpoints, for
example, if you wanted to add a League of Legends API to this project, you would create a child class of `GameRouter` and
override each of the endpoint methods with their own API calls to get league data. See more info in the `GameRouter` class itself
"""

from __future__ import annotations

from typing import Optional

from ..app.resources import Event, Match, Player, Team


class GameRouter:
    """Data structure that contains all the functions that can be overriden for a specific game's API

    Functions:
        - `get_player`
        - `get_player_matches`
        - `get_player_teams`
        - `get_team`
        - `get_team_matches`
        - `get_team_players`
        - `get_match`
        - `get_event`
        - `get_event_matches`
        - `get_event_teams`
    """

    @staticmethod
    def is_implemented(router: GameRouter, method: str) -> bool:
        """Detemines whether the given subclassed router implements a method, or whether it is still the default
        method

        Args:
            router (GameRouter): The `GameRouter` subclass to check
            method (str): The method to check

        Returns:
            bool: Whether the subclassed router has a custom implementation of the method
        """
        return getattr(router, method) != getattr(GameRouter, method)

    @staticmethod
    def get_player(player_id: int) -> Optional[Player]:
        """This method should be overridden if you want to allow people to access individual player data from your
        game's endpoint

        Args:
            player_id (str): The player_id (not source_id) of the player in the database. This should correspond to the ID
            used to access the player's data from whatever external site or API you are using to scrape the data from

        Returns:
            Optional[Player]: the player data returned (or None if the player does not exist)
        """
        return None

    @staticmethod
    def get_player_matches(player_id: int, page: int) -> list[Match]:
        """This method should be overridden if you want to allow people to access a list of matches that a specific player
        has played in

        Args:
            player_id (str): The id of the player to get the matches for
            page (int): The page of matches to get. 20 matches per page

        Returns:
            list[Match]: a list of the matches that the player has played (or None if the )
        """
        return None

    @staticmethod
    def get_player_teams(player_id: int) -> list[Team]:
        """This method should be overridden if you want to allow users to access a list of teams a player has been a part
        of

        Args:
            player_id (int): _description_

        Returns:
            list[Team]: list of player teams, or None if this method is not supported
        """
        return None

    @staticmethod
    def get_team(team_id: int) -> Optional[Team]:
        """This method should be overridden if you want to allow users to access data about a specific team

        Args:
            team_id (int): the ID of the team to get information about

        Returns:
            Team: The team object containing the team data, or None if the team_id cannot be found
        """
        return None

    @staticmethod
    def get_team_matches(team_id: int, page: int) -> list[Match]:
        return []

    @staticmethod
    def get_team_players(team_id: int) -> list[Player]:
        return []

    @staticmethod
    def get_match(match_id: int) -> Optional[Match]:
        return None

    @staticmethod
    def get_event(event_id: int) -> Optional[Event]:
        return None

    @staticmethod
    def get_event_matches(event_id: int) -> list[Match]:
        return []

    @staticmethod
    def get_event_teams(event_id: int) -> list[Team]:
        return []
