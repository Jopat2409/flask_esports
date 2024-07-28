from __future__ import annotations

class Source:

    def __init__(self, source_name: str, source_suffixes: list[str] = [], is_root: bool = False):
        self.sources = [f"{source_name}_{suffix}" for suffix in source_suffixes] or [source_name]
        self.api_endpoint = ("/" if is_root else f"/{source_name}")

    def get_querystring(self) -> str:
        return (f"source IN {self.sources}".replace("'", '"') if len(self.sources) > 1 else f'source = "{self.sources[0]}"')

    def get_endpoint(self) -> str:
        return self.api_endpoint

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
