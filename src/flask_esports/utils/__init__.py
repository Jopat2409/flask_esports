"""Helper functions and classes for the esports flask API
"""
import re

def is_valid_endpoint(api_endpoint: str) -> bool:
    """Checks a given string for validity if it were to be used as a flask endpoint

    Args:
        api_endpoint (str): The endpoint to validate

    Returns:
        bool: True if the string is a valid endpoint, or False if it is not.
    """
    return False if re.match("^/[a-zA-Z0-9_-]*$", api_endpoint) is None else True
