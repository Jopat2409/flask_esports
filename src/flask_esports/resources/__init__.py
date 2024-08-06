"""This module contains the dataclasses of all the resources that can be returned from the API fetching
functions.

These are:
    - `Player`
    - `Match`
    - `Team`
    - `Event`

Additionally, some dataclasses are implemented to add additional info to the previous 4 atomic classes:
    - `TeamPlayer` contains data about a player, as well as the joining / leaving data for the player
    - `PlayerTeam` contains data about a team, as well as the joining / leaving data for the player
"""

from .player import Player
from .match import Match
from .team import Team
from .event import Event

from .associations import TeamPlayer, PlayerTeam

__all__ = [Player, Match, Team, Event, TeamPlayer, PlayerTeam]
