from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.bean import Bean, Beans, BeanSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.bean import BeanService

app = APIRouter()
service = BeanService("bean-products")


@app.get(
    "",
    name="Get all beans",
    responses={**ServiceResponse(Beans).multi("get_beans", obj="Bean")},
)
def get_beans():
    try:
        # ? Get total of bean, and the beans data
        count, beans = service.get_beans()

        # ? Check if beans is not empty
        if beans:
            # * Return 200 if beans is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all beans",
                    "total": count,
                    "data": beans.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if beans is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Beans not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all bean",
        )


@app.post(
    "/search",
    name="Get all beans",
    responses={**ServiceResponse(Beans).multi("get_beans", obj="Bean")},
)
def search_beans(payload: SearchSchema):
    try:
        # ? Get total of bean, and the beans data
        count, beans = service.search_beans(payload)

        # ? Check if beans is not empty
        if beans:
            # * Return 200 if beans is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all beans",
                    "total": count,
                    "data": beans.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if beans is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Beans not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all bean",
        )


@app.get(
    "/{id}", responses={**ServiceResponse(Bean).get("get_bean", obj="Bean")}
)
def get_bean(id: str = Path(..., description="Bean id")):
    try:
        # ? Check if bean is not empty
        if bean := service.get_bean(id):
            # * Return 200 if beans is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": bean.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if bean is empty, which means there is no bean with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Bean not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get bean",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Bean).creation("add_bean", obj="Bean")},
)
def add_bean(data: BeanSchema):
    try:
        bean = service.add_bean(data)

        # * Return 201, and the bean
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Bean created successfully",
                "data": bean.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add bean",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Bean).update("update_bean", obj="Bean")},
)
def update_bean(data: BeanSchema, id: str = Path(..., description="Bean id")):
    try:
        # ? Check if bean is updated successfully
        if service.update_bean(id, data):
            # * Return 200, and id of the bean
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Bean updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no bean with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Bean not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add bean",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Bean).delete("delete_bean", obj="Bean")},
)
def delete_bean(id: str = Path(..., description="Bean id")):
    try:
        # ? Check if bean is deleted successfully
        if service.delete_bean(id):
            # * Return 200, and id of the bean
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Bean deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no bean with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Bean not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add bean",
        )
