from __future__ import annotations


class SourceId:
    def __init__(self, src: str, id_: int) -> None:
        """Creates a sourceId object given the site source and the ID of the site resource

        Args:
            src (str): The string of the source used (tf2, valorant etc.)
            id_ (int): The actual ID of the source (for example with steam games it would be the steam64 ID)
        """
        self.source = (src, int(id_))

    def get_source(self) -> str:
        """Gets the source of the ID

        Returns:
            str: The source
        """
        return self.source[0]

    def get_id(self) -> int:
        """Gets the ID of the resource on the specific site

        Returns:
            int: The ID of the resource
        """
        return self.source[1]

    def __eq__(self, other: SourceId) -> bool:
        return self.source == other.source
