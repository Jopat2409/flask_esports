"""Encapsulates all the data required to be returned from any game implementing any endpoints that return some sort of
information about teams

`Team` is used as the return type for get_team (/team/team_id)
`PlayerTeam` is used as the return type for get_player_teams (/player/player_id/teams)
`EventTeam` is used as the return type for get_event_teams (/event/event_id/teams)
"""
from __future__ import annotations
from enum import IntEnum

from esports_api.source import SourceId

class Role(IntEnum):
    HEAD_COACH = 1
    ASSISTANT_COACH = 2
    PERFORMANCE_COACH = 3
    MANAGER = 4
    ANALYST = 5
    COACH = 6

    def __str__(self) -> str:
        return f"{self.name.replace('_', ' ').title()}"

class Team:
    """Encapsulates all the data that should be returned from a call to get_team (/team/id) endpoint
    """

    def __init__(self, team_id: SourceId, name: str, tag: str, logo: str, region: str) -> None:
        self.id = team_id
        self.name = name
        self.tag = tag
        self.logo = logo
        self.region = region
        self.current_roster = []
        self.current_staff = []

    def add_player(self, player_id: int, display_name: str = None, sub: bool = False, active: bool = True) -> None:
        self.current_roster.append({"id": player_id, "name": display_name, "substitute": sub, "inactive": not active})

    def add_staff(self, staff_id: int, display_name: str, role: Role):
        self.current_staff.append({"id": staff_id, "name": display_name, "role": str(role)})

    def to_dict(self) -> dict:
        return {
            "id": self.id.get_id(),
            "name": self.name,
            "display-tag": self.tag,
            "logo-url": self.logo,
            "region": self.region,
            "current-roster": self.current_roster,
            "current-staff": self.current_staff
        }

    def __eq__(self, other: Team) -> bool:
        return isinstance(other, Team) and\
                self.id == other.id and\
                self.name == other.name and\
                self.logo == other.logo and\
                self.region == other.region

class PlayerTeam:

    def __init__(self, team_id: SourceId, name: str, joined_at: float = None, left_at: float = None) -> None:
        self.team_id = team_id
        self.name = name
        self.joined = joined_at
        self.left = left_at

    def to_dict(self) -> dict:
        return {
            "id": self.team_id,
            "name": self.name,
            "joined-at": self.joined,
            "left-at": self.left
        }
