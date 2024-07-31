"""Custom classes used to make implementing new games to the API a much easier ordeal

The `DataSource` class contains all the static methods that should can be overridden to create your own API endpoints, for
example, if you wanted to add a League of Legends API (god forbid) to this project, you would create a child class of `DataSource` and
override each of the endpoint methods with their own API calls to get league data. See more info in the `DataSource` class itself
"""

from __future__ import annotations

from typing import Optional

from ..app.resources import Event, Match, Player, Team


class DataSource:
    """Represents a single source of data for a custom API. Can use another API, can use web scraping, can even be
    custom calls to your own database. If this is the case, make sure to set the flag `db.USE_CUSTOM` (WIP) so that the
    default database is not used

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
    def is_implemented(source: DataSource, method: str) -> bool:
        """Detemine whether a `DataSource` overrides the given method

        Args:
            source (DataSource): The `GameRouter` subclass to check
            method (str): The method to check

        Returns:
            bool: Whether the `DataSource` has a custom implementation of `method`
        """
        try:
            return getattr(source, method) != getattr(DataSource, method)
        except AttributeError:
            # Log this error
            return False

    @staticmethod
    def get_player(player_id: int) -> Optional[Player]:
        """Get data from the source about the player represented by the `player_id` given

        Args:
            player_id (str): The player_id of the player. This should correspond to the ID
            used to access the player's data from whatever external site or API you are using to scrape the data from

        Returns:
            Optional[Player]: the player data returned (or None if the player does not exist)
        """
        return None

    @staticmethod
    def get_player_matches(player_id: int, page: int) -> list[Match]:
        """Get data from the source about the matches that the player represented by the `player_id` has been a part of.
        Paginated, with 20 matches per page

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
