from __future__ import annotations

from typing import Optional


class Resource:
    """A class that derives from Resource is a dataclass that contains information about some kind of object that an
    end user might want to query using the API.

    Each subclass of Resource should override the function `to_dict`, which should return all the contained data in
    dictionary form, with all data returned being serializable. You should always make a call to `super().to_dict()` as
    each additional subclass layer should ADD to the existing serialization, not create its own

    Additionally, each Resource subclass has the ability to specify a custom Resource to use as the additional_info parameter.
    This parameter is used
    """

    def __init__(self, additional_info: Optional[Resource] = None) -> None:
        self.additional_info_res = additional_info

    def to_dict(self) -> dict:
        return (
            {}
            if self.additional_info_res is None
            else self.additional_info_res.to_dict()
        )
