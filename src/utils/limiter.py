from math import ceil

from fastapi import Request, Response, HTTPException, status


async def service_name_identifier(request: Request) -> str:
    service = request.client.host  # type: ignore
    return service


async def limiter_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too Many Requests. Retry after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )
