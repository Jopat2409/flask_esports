from typing import Optional

from .resource import Resource
from .player import Player


class TeamPlayer:
    def __init__(
        self, player: Player, joined_at: float, left_at: Optional[float]
    ) -> None:
        self.player = player
        self.joined = joined_at or None
        self.left = left_at or None

    def to_dict(self):
        return {"joined-at": self.joined, "left-at": self.left, **self.player.to_dict()}
