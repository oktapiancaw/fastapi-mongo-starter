from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.brew_method import BrewMethod, BrewMethods, BrewMethodSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.brew_method import BrewMethodService

app = APIRouter()
service = BrewMethodService("brew-methods")


@app.get(
    "",
    name="Get all Brew Methods",
    responses={
        **ServiceResponse(BrewMethods).multi(
            "get_brew_methods", obj="Brew Method"
        )
    },
)
def get_brew_methods():
    try:
        # ? Get total of brew_method, and the brew_methods data
        count, brew_methods = service.get_brew_methods()

        # ? Check if brew_methods is not empty
        if brew_methods:
            # * Return 200 if brew_methods is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all Brew Methods",
                    "total": count,
                    "data": brew_methods.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if brew_methods is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Brew Methods not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all Brew Method",
        )


@app.post(
    "/search",
    name="Get all Brew Methods",
    responses={
        **ServiceResponse(BrewMethods).multi(
            "get_brew_methods", obj="Brew Method"
        )
    },
)
def search_brew_methods(payload: SearchSchema):
    try:
        # ? Get total of brew_method, and the brew_methods data
        count, brew_methods = service.search_brew_methods(payload)

        # ? Check if brew_methods is not empty
        if brew_methods:
            # * Return 200 if brew_methods is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all Brew Methods",
                    "total": count,
                    "data": brew_methods.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if brew_methods is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Brew Methods not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all Brew Method",
        )


@app.get(
    "/{id}",
    responses={
        **ServiceResponse(BrewMethod).get("get_brew_method", obj="Brew Method")
    },
)
def get_brew_method(id: str = Path(..., description="Brew Method id")):
    try:
        # ? Check if brew_method is not empty
        if brew_method := service.get_brew_method(id):
            # * Return 200 if brew_methods is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": brew_method.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if brew_method is empty, which means there is no brew_method with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Brew Method not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get Brew Method",
        )


@app.post(
    "",
    status_code=201,
    responses={
        **ServiceResponse(BrewMethod).creation(
            "add_brew_method", obj="Brew Method"
        )
    },
)
def add_brew_method(data: BrewMethodSchema):
    try:
        brew_method = service.add_brew_method(data)

        # * Return 201, and the brew_method
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Brew Method created successfully",
                "data": brew_method.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Brew Method",
        )


@app.put(
    "/{id}",
    responses={
        **ServiceResponse(BrewMethod).update(
            "update_brew_method", obj="Brew Method"
        )
    },
)
def update_brew_method(
    data: BrewMethodSchema, id: str = Path(..., description="Brew Method id")
):
    try:
        # ? Check if brew_method is updated successfully
        if service.update_brew_method(id, data):
            # * Return 200, and id of the brew_method
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Brew Method updated successfully",
                    "id": id,
                },
            )

        # ! Return 404 if updated is return 0, which means there is no brew_method with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Brew Method not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Brew Method",
        )


@app.delete(
    "/{id}",
    responses={
        **ServiceResponse(BrewMethod).delete(
            "delete_brew_method", obj="Brew Method"
        )
    },
)
def delete_brew_method(id: str = Path(..., description="Brew Method id")):
    try:
        # ? Check if brew_method is deleted successfully
        if service.delete_brew_method(id):
            # * Return 200, and id of the brew_method
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Brew Method deleted successfully",
                    "id": id,
                },
            )

        # ! Return 404 if deleted is return 0, which means there is no brew_method with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Brew Method not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Brew Method",
        )
