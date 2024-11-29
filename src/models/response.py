from typing import Any

from pydantic import create_model


class ServiceResponse:

    def __init__(self, model: Any, auth: bool = False) -> None:
        self.model = model
        self.auth = auth

    def basic(self, route: str) -> dict:
        """
        Generate a basic response, which is a dictionary of common response codes and models.

        Contains:
        - 400 Bad Request
        - 500 Internal Server Error

        :param route: The path of the route
        :return: A dictionary of common response codes and models
        """
        return {
            # 400: {
            #     "model": create_model(
            #         route, code=(int, 400), message=(str, "Bad Request")
            #     ),
            #     "description": "Occurs when the request you make does not match or is invalid",
            # },
            500: {
                "model": create_model(
                    route,
                    message=(str, "Internal Server Error"),
                ),
                "description": "Occurs when there is an engine or lib error in the engine",
            },
        }

    def get(
        self,
        route: str,
        model: Any = None,
        obj: str = "Data",
        auth: bool = False,
        exclude_codes: list = [],
        **kwargs,
    ) -> dict:
        """
        Generate a response for a get request, which is a dictionary of common response codes and models.

        Contains:
        - 200 Success
        - 404 Not Found

        :param route: The path of the route
        :param model: The model to use for the response
        :param obj: The object name to use for the response
        :param auth: Whether or not the route requires authentication
        :param exclude_codes: A list of codes to exclude from the response
        :return: A dictionary of common response codes and models
        """
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    message=(str, "Success"),
                    data=(model if model else self.model, ...),
                ),
                "description": "Success get data",
            },
            404: {
                "model": create_model(route, message=(str, f"{obj} not found")),
            },
            **self.basic(route),
            **kwargs,
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]

        if auth or self.auth:
            response[401] = {
                "model": create_model(route, message=(str, "Unauthorized"))
            }

        return response

    def multi(
        self,
        route: str,
        model: Any = None,
        obj: str = "Data",
        auth: bool = False,
        exclude_codes: list = [],
        **kwargs,
    ) -> dict:
        """
        Generate a response for a multi request, which is a dictionary of common response codes and models.

        Contains:
        - 200 OK
        - 404 Not Found
        - 401 Unauthorized (optional)

        :param route: The path of the route
        :param model: The model to use for the response
        :param obj: The object name to use for the response
        :param auth: Whether or not the route requires authentication
        :param exclude_codes: A list of codes to exclude from the response
        :return: A dictionary of common response codes and models
        """
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    message=(str, f"Success get all {obj}"),
                    data=(model if model else self.model, ...),
                    total=(int, 10),
                ),
            },
            404: {
                "model": create_model(route, message=(str, f"{obj} not found")),
            },
            **self.basic(route),
            **kwargs,
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]

        if auth or self.auth:
            response[401] = {
                "model": create_model(route, message=(str, "Unauthorized"))
            }

        return response

    def creation(
        self,
        route: str,
        model: Any = None,
        obj: str = "Data",
        auth: bool = False,
        exclude_codes: list = [],
        **kwargs,
    ) -> dict:
        """
        Generate a response for a create request, which is a dictionary of common response codes and models.

        Contains:
        - 201 Created
        - 401 Unauthorized

        :param route: The path of the route
        :param model: The model to use for the response
        :param obj: The object name to use for the response
        :param auth: Whether or not the route requires authentication
        :param exclude_codes: A list of codes to exclude from the response
        :return: A dictionary of common response codes and models
        """
        response: dict = {
            201: {
                "model": create_model(
                    route,
                    message=(str, f"{obj} created successfully"),
                    data=(model if model else self.model, ...),
                ),
            },
            **self.basic(route),
            **kwargs,
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]

        if auth or self.auth:
            response[401] = {
                "model": create_model(route, message=(str, "Unauthorized"))
            }

        return response

    def update(
        self,
        route: str,
        model: Any = None,
        obj: str = "Data",
        auth: bool = False,
        exclude_codes: list = [],
        **kwargs,
    ) -> dict:
        """
        Generate a response for a update request, which is a dictionary of common response codes and models.

        Contains:
        - 200 OK
        - 204 No Content
        - 401 Unauthorized (optional)

        :param route: The path of the route
        :param model: The model to use for the response
        :param obj: The object name to use for the response
        :param auth: Whether or not the route requires authentication
        :param exclude_codes: A list of codes to exclude from the response
        :return: A dictionary of common response codes and models
        """
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    message=(str, f"{obj} updated successfully"),
                    id=(str, ...),
                ),
            },
            404: {
                "model": create_model(route, message=(str, f"{obj} not found")),
            },
            # 204: {
            #     "model": create_model(
            #         route,
            #         message=(str, f"{obj} updated successfully"),
            #     ),
            # },
            **self.basic(route),
            **kwargs,
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]

        if auth or self.auth:
            response[401] = {
                "model": create_model(route, message=(str, "Unauthorized"))
            }

        return response

    def delete(
        self,
        route: str,
        model: Any = None,
        obj: str = "Data",
        auth: bool = False,
        exclude_codes: list = [],
        **kwargs,
    ) -> dict:
        """
        Generate a response for a delete request, which is a dictionary of common response codes and models.

        Contains:
        - 200 Success
        - 204 Success
        - 400 Bad Request
        - 401 Unauthorized (optional)
        - 500 Internal Server Error

        :param route: The path of the route
        :param model: The model to use for the response
        :param obj: The object name to use for the response
        :param auth: Whether or not the route requires authentication
        :param exclude_codes: A list of codes to exclude from the response
        :return: A dictionary of common response codes and models
        """
        response: dict = {
            200: {
                "model": create_model(
                    route,
                    message=(str, f"{obj} deleted successfully"),
                    id=(str, ...),
                ),
            },
            404: {
                "model": create_model(route, message=(str, f"{obj} not found")),
            },
            # 204: {
            #     "model": create_model(
            #         route,
            #         message=(str, f"{obj} delete successfully"),
            #     ),
            # },
            **self.basic(route),
            **kwargs,
        }

        if exclude_codes:
            for code in exclude_codes:
                del response[code]

        if auth or self.auth:
            response[401] = {
                "model": create_model(route, message=(str, "Unauthorized"))
            }

        return response
