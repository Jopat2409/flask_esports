"""Useful decorator functions to reduce code duplication in the API coedebase"""

from ..api.response import ResponseFactory


def require_int(arg: str, error_message: str) -> callable:
    """Decorator that automatically takes in a route's argument (arg) and returns an error response if the
    argument cannot be converted to an integer / is not in integer form.

    Useful in situations where your route takes in a single database ID, and you need to ensure that this ID is
    integer compatible at the start of the route

    Args:
        arg (str): The argument that should be a valid integer
        error_message (str): The error message to return using `ResponseFactory.error` if the argument is not valid
    """

    def require_int(func) -> callable:
        def inner(*args, **kwargs):
            try:
                kwargs[arg] = float(kwargs[arg])
                # Trigger exception return
                if int(kwargs[arg]) != kwargs[arg]:
                    raise ValueError("Float passed into function requiring integer")
                kwargs[arg] = int(kwargs[arg])
            except ValueError:
                return ResponseFactory.error(error_message)
            return (
                func(*args, **kwargs)
                if int(kwargs[arg]) == kwargs[arg]
                else ResponseFactory.error(error_message)
            )

        return inner

    return require_int
