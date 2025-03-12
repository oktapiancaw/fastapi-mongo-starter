from fastapi import APIRouter, Request, HTTPException, Depends, Path, status
from fastapi.responses import JSONResponse

from src.utils.token import JWTBearer
from src.models.response import ServiceResponse
from src.models.token import RequestTokenSchema, RequestToken, RequestTokenExtract
from src.routes.services.token import TokenService

app = APIRouter()
service = TokenService()


@app.post(
    "",
    name="Request a token",
    responses={**ServiceResponse(RequestToken).creation("request_token", obj="Token")},
)
def request_token(data: RequestTokenSchema):
    try:
        payload = service.create_token(data=data)

        # * Return 201, and the token
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Token created successfully",
                "data": payload.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed add post"
        )


@app.get(
    "",
    name="check a token",
    dependencies=[
        Depends(JWTBearer()),
    ],
    responses={
        **ServiceResponse(RequestTokenExtract).get(
            "check_token", obj="Token", auth=True
        )
    },
)
def check_token(request: Request):
    try:
        cred = request.state.credentials
        payload = RequestTokenExtract.model_validate(cred)

        # * Return 200 if token is valid
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Success",
                "data": payload.model_dump(by_alias=True),
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed add post"
        )
