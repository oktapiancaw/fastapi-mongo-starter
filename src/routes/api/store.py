from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.store import Store, Stores, StoreSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.store import StoreService

app = APIRouter()
service = StoreService("stores")


@app.get(
    "",
    name="Get all stores",
    responses={**ServiceResponse(Stores).multi("get_stores", obj="Store")},
)
def get_stores():
    try:
        # ? Get total of store, and the stores data
        count, stores = service.get_stores()

        # ? Check if stores is not empty
        if stores:
            # * Return 200 if stores is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all stores",
                    "total": count,
                    "data": stores.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if stores is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Stores not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all store",
        )


@app.post(
    "/search",
    name="Get all stores",
    responses={**ServiceResponse(Stores).multi("get_stores", obj="Store")},
)
def search_stores(payload: SearchSchema):
    try:
        # ? Get total of store, and the stores data
        count, stores = service.search_stores(payload)

        # ? Check if stores is not empty
        if stores:
            # * Return 200 if stores is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all stores",
                    "total": count,
                    "data": stores.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if stores is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Stores not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all store",
        )


@app.get(
    "/{id}",
    responses={**ServiceResponse(Store).get("get_store", obj="Store")},
)
def get_store(id: str = Path(..., description="Store id")):
    try:
        # ? Check if store is not empty
        if store := service.get_store(id):
            # * Return 200 if stores is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": store.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if store is empty, which means there is no store with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Store not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get store",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Store).creation("add_store", obj="Store")},
)
def add_store(data: StoreSchema):
    try:
        store = service.add_store(data)

        # * Return 201, and the store
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Store created successfully",
                "data": store.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add store",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Store).update("update_store", obj="Store")},
)
def update_store(
    data: StoreSchema, id: str = Path(..., description="Store id")
):
    try:
        # ? Check if store is updated successfully
        if service.update_store(id, data):
            # * Return 200, and id of the store
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Store updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no store with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Store not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add store",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Store).delete("delete_store", obj="Store")},
)
def delete_store(id: str = Path(..., description="Store id")):
    try:
        # ? Check if store is deleted successfully
        if service.delete_store(id):
            # * Return 200, and id of the store
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Store deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no store with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Store not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add store",
        )
