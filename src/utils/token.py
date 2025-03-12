from datetime import timedelta, timezone, datetime

import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from src.configs import config, LOGGER


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(
            request
        )  # type: ignore
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            request.state.credentials = self.decodeJWT(credentials.credentials)
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def decodeJWT(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, config.app.auth_secret, algorithms=["HS256"]
            )
            return decoded_token
        except:
            return {}

    def verify_jwt(self, jwtoken: str) -> bool:

        try:
            jwtoken = jwtoken.replace("Bearer ", "")
            payload = self.decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            if payload["exp"] >= datetime.now().timestamp():
                return True
            return False
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.app.auth_secret, algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        LOGGER.exception(e)
        raise
