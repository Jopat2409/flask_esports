
class Source:

    def __init__(self, source_name: str, source_suffixes: list[str] = [], is_root: bool = False):
        self.sources = [f"{source_name}_{suffix}" for suffix in source_suffixes] or [source_name]
        self.api_endpoint = f"/{source_name}" if is_root else "/"

    def get_querystring(self) -> str:
        return f"source IN {self.sources}" if len(self.sources) > 1 else f"source = {self.source}"

    def get_endpoint(self) -> str:
        return self.api_endpoint
