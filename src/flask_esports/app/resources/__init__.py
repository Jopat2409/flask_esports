"""This module contains the dataclasses of all the resources that can be returned from the API fetching
functions.

These are:
    - `Player`
    - `Match`
    - `Team`
    - `Event`
"""

from .player import Player
from .match import Match
from .team import Team
from .event import Event

__all__ = [Player, Match, Team, Event]
