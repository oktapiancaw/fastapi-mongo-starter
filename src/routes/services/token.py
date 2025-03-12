from datetime import timedelta

from src.configs import LOGGER
from src.models.token import RequestTokenSchema, RequestToken

from src.utils.token import create_access_token


class TokenService:

    def __init__(self) -> None:
        pass

    def create_token(self, data: RequestTokenSchema) -> RequestToken:
        try:
            token = create_access_token(
                data=data.model_dump(), expires_delta=timedelta(minutes=30)
            )
            payload = RequestToken(**data.model_dump(), token=token)
            return payload
        except Exception:
            LOGGER.exception("Failed create token")
            raise
