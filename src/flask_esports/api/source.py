"""Custom classes used to make implementing new games to the API a much easier ordeal

The `DataSource` class contains all the static methods that should can be overridden to create your own API endpoints, for
example, if you wanted to add a League of Legends API (god forbid) to this project, you would create a child class of `DataSource` and
override each of the endpoint methods with their own API calls to get league data. See more info in the `DataSource` class itself
"""

from __future__ import annotations

from typing import Optional

from ..app.resources import Event, Match, Player, Team
from ..app.resources.associations import TeamPlayer


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
        return []

    @staticmethod
    def get_player_teams(player_id: int) -> list[Team]:
        """Get data from the source regarding the previous and current teams that the given player has played on /
        been a part of

        Args:
            player_id (int): The id of the player to get the teams for

        Returns:
            list[Team]:  list of the teams that the player has played on (or None if the )
        """
        return []

    @staticmethod
    def get_team(team_id: int) -> Optional[Team]:
        """Get data from the source regarding a team, given the `team_id` of the team

        Args:
            team_id (int): the ID of the team to get information about

        Returns:
            Optional[Team]: The team object containing the team data, or None if the `team_id` cannot be found
        """
        return None

    @staticmethod
    def get_team_matches(team_id: int, page: int) -> list[Match]:
        """Get data from the source regarding the matches that a given team has played. Paginated with 20 matches
        per page

        Args:
            team_id (int): The ID of the team to get matches for
            page (int): The page to get (1-indexed)

        Returns:
            list[Match]: The matches
        """
        return []

    @staticmethod
    def get_team_players(team_id: int) -> list[TeamPlayer]:
        """Get data from the source regarding the player history of a given team. The information returned should be
        the player's data (although it does not have to be completed), the epoch of the join date of the player, and
        the epoch of the leaving date (or `None` if it is the current team)

        Args:
            team_id (int): The ID of the team to get the player history for

        Returns:
            list[TeamPlayer]: History of players on the team
        """
        return []

    @staticmethod
    def get_match(match_id: int) -> Optional[Match]:
        """Get data from the source regarding the information of the given match

        Args:
            match_id (int): The ID of the match to get the details of

        Returns:
            Optional[Match]: The match data (or `None` if it does not exist)
        """
        return None

    @staticmethod
    def get_event(event_id: int) -> Optional[Event]:
        """Get data from the source about the event corresponding to the `event_id`

        Args:
            event_id (int): _description_

        Returns:
            Optional[Event]: _description_
        """
        return None

    @staticmethod
    def get_event_matches(event_id: int, page: int = 1) -> list[Match]:
        return []

    @staticmethod
    def get_event_teams(event_id: int) -> list[Team]:
        return []
