from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.wiki import Wiki, Wikis, WikiSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.wiki import WikiService

app = APIRouter()
service = WikiService("wikis")


@app.get(
    "",
    name="Get all wikis",
    responses={**ServiceResponse(Wikis).multi("get_wikis", obj="Wiki")},
)
def get_wikis():
    try:
        # ? Get total of wiki, and the wikis data
        count, wikis = service.get_wikis()

        # ? Check if wikis is not empty
        if wikis:
            # * Return 200 if wikis is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all wikis",
                    "total": count,
                    "data": wikis.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if wikis is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Wikis not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all wiki",
        )


@app.post(
    "/search",
    name="Get all wikis",
    responses={**ServiceResponse(Wikis).multi("get_wikis", obj="Wiki")},
)
def search_wikis(payload: SearchSchema):
    try:
        # ? Get total of wiki, and the wikis data
        count, wikis = service.search_wikis(payload)

        # ? Check if wikis is not empty
        if wikis:
            # * Return 200 if wikis is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all wikis",
                    "total": count,
                    "data": wikis.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if wikis is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Wikis not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all wiki",
        )


@app.get(
    "/{id}",
    responses={**ServiceResponse(Wiki).get("get_wiki", obj="Wiki")},
)
def get_wiki(id: str = Path(..., description="Wiki id")):
    try:
        # ? Check if wiki is not empty
        if wiki := service.get_wiki(id):
            # * Return 200 if wikis is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": wiki.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if wiki is empty, which means there is no wiki with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Wiki not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get wiki",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Wiki).creation("add_wiki", obj="Wiki")},
)
def add_wiki(data: WikiSchema):
    try:
        wiki = service.add_wiki(data)

        # * Return 201, and the wiki
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Wiki created successfully",
                "data": wiki.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add wiki",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Wiki).update("update_wiki", obj="Wiki")},
)
def update_wiki(data: WikiSchema, id: str = Path(..., description="Wiki id")):
    try:
        # ? Check if wiki is updated successfully
        if service.update_wiki(id, data):
            # * Return 200, and id of the wiki
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Wiki updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no wiki with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Wiki not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add wiki",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Wiki).delete("delete_wiki", obj="Wiki")},
)
def delete_wiki(id: str = Path(..., description="Wiki id")):
    try:
        # ? Check if wiki is deleted successfully
        if service.delete_wiki(id):
            # * Return 200, and id of the wiki
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Wiki deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no wiki with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Wiki not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add wiki",
        )
