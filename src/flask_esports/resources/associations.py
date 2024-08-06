from __future__ import annotations

from typing import Optional

from .player import Player
from .team import Team


class TeamPlayer:
    """Class containing information about a team's player. It includes data about the player itself, as well as the
    date (epoch in seconds) at which the player joined and left the team.

    If the player has not left the team as they are on its current roster (or they are benched), then the `left_at` parameter
    should be set to None

    Similar to `PlayerTeam`, except this class contains information about the team itself rather than the player
    """

    def __init__(
        self, player: Player, joined_at: float, left_at: Optional[float]
    ) -> None:
        """Store information regarding a player for a particular team.

        Args:
            player (Player): The player to hold the information about
            joined_at (float): The epoch in seconds that the player joined the team
            left_at (Optional[float]): The epoch in seconds that the player left the team (or `None` if they haven't left)
        """
        self.player = player
        self.joined = joined_at or None
        self.left = left_at or None

    def __eq__(self, other: TeamPlayer) -> bool:
        return (
            isinstance(other, TeamPlayer)
            and other.joined == self.joined
            and other.left == self.left
            and other.player == self.player
        )

    def to_dict(self):
        return {"joined-at": self.joined, "left-at": self.left, **self.player.to_dict()}


class PlayerTeam:
    """Class containing information about a player's team. It includes data about the team itself, as well as the
    date (epoch in seconds) at which the player joined and left the team.

    If the player has not left the team as they are on its current roster (or they are benched), then the `left` attribute
    should be set to None

    Similar to `TeamPlayer`, except this class contains information about the team itself rather than the player
    """

    def __init__(self, team: Team, joined_at: float, left_at: Optional[float]) -> None:
        self.team = team
        self.joined = joined_at or None
        self.left = left_at or None

    def to_dict(self) -> dict:
        return {"joined-at": self.joined, "left-at": self.left, **self.team.to_dict()}
