"""Generate standard response messages throught the whole application

If the response style of the application should be changed, it can be done so by changing the methods here
"""
from flask import jsonify, Response

class ResponseFactory:
    """Static class containing functions used to generate API responses.\n
    Use:
    - `ResponseFactory.success` for a successful request
    - `ResponseFactory.error` for an unsuccessful request
    - `ResponseFactory.conditional` to simplify conditional responses
    """

    @staticmethod
    def error(error_message: str) -> Response:
        """Creates a response indicating that an internal server error has occurred, or that there was some
        issue with the input parameters for the route

        Args:
            error_message (str): The message to include in the response indicating what went wrong with the request

        Returns:
            Response: A flask `Response` indicating an unsuccessful request
        """
        return jsonify({"success": False, "data": {"error-message": error_message}})

    @staticmethod
    def success(data: list | dict) -> Response:
        """Creates a response indicating a successful request to the API

        Args:
            data (list | dict): The data to return to the requesting browser

        Returns:
            Response: A flask `Response` indicating a successful request, with any data
        """
        return jsonify({"success": True, "data": data})

    @staticmethod
    def conditional(condition: bool, data: dict | list, msg: str = "There was an error") -> Response:
        """Creates an `error` response if the condition is false, otherwise creates a `success` response

        Args:
            condition (bool): Whether the request was successful
            data (dict | list): Data to return (on success)
            msg (str, optional): Error message to return (on failure). Defaults to "There was an error".

        Returns:
            Response: The generated flask `Response` based on the `condition`
        """
        return jsonify({"success": True if condition else False, "data": data if condition else {"error-message": msg}})
