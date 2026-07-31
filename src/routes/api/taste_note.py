from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.taste_note import TasteNote, TasteNotes, TasteNoteSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.taste_note import TasteNoteService

app = APIRouter()
service = TasteNoteService("sca-flavour-wheels")


@app.get(
    "",
    name="Get all Taste notes",
    responses={
        **ServiceResponse(TasteNotes).multi("get_taste_notes", obj="Taste note")
    },
)
def get_taste_notes():
    try:
        # ? Get total of taste_note, and the taste_notes data
        count, taste_notes = service.get_taste_notes()

        # ? Check if taste_notes is not empty
        if taste_notes:
            # * Return 200 if taste_notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all Taste notes",
                    "total": count,
                    "data": taste_notes.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if taste_notes is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Taste notes not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all Taste note",
        )


@app.post(
    "/search",
    name="Get all Taste notes",
    responses={
        **ServiceResponse(TasteNotes).multi("get_taste_notes", obj="Taste note")
    },
)
def search_taste_notes(payload: SearchSchema):
    try:
        # ? Get total of taste_note, and the taste_notes data
        count, taste_notes = service.search_taste_notes(payload)

        # ? Check if taste_notes is not empty
        if taste_notes:
            # * Return 200 if taste_notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all Taste notes",
                    "total": count,
                    "data": taste_notes.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if taste_notes is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Taste notes not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all Taste note",
        )


@app.get(
    "/{id}",
    responses={
        **ServiceResponse(TasteNote).get("get_taste_note", obj="Taste note")
    },
)
def get_taste_note(id: str = Path(..., description="Taste note id")):
    try:
        # ? Check if taste_note is not empty
        if taste_note := service.get_taste_note(id):
            # * Return 200 if taste_notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": taste_note.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if taste_note is empty, which means there is no taste_note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Taste note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get Taste note",
        )


@app.post(
    "",
    status_code=201,
    responses={
        **ServiceResponse(TasteNote).creation(
            "add_taste_note", obj="Taste note"
        )
    },
)
def add_taste_note(data: TasteNoteSchema):
    try:
        taste_note = service.add_taste_note(data)

        # * Return 201, and the taste_note
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Taste note created successfully",
                "data": taste_note.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Taste note",
        )


@app.put(
    "/{id}",
    responses={
        **ServiceResponse(TasteNote).update(
            "update_taste_note", obj="Taste note"
        )
    },
)
def update_taste_note(
    data: TasteNoteSchema, id: str = Path(..., description="Taste note id")
):
    try:
        # ? Check if taste_note is updated successfully
        if service.update_taste_note(id, data):
            # * Return 200, and id of the taste_note
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Taste note updated successfully",
                    "id": id,
                },
            )

        # ! Return 404 if updated is return 0, which means there is no taste_note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Taste note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Taste note",
        )


@app.delete(
    "/{id}",
    responses={
        **ServiceResponse(TasteNote).delete(
            "delete_taste_note", obj="Taste note"
        )
    },
)
def delete_taste_note(id: str = Path(..., description="Taste note id")):
    try:
        # ? Check if taste_note is deleted successfully
        if service.delete_taste_note(id):
            # * Return 200, and id of the taste_note
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Taste note deleted successfully",
                    "id": id,
                },
            )

        # ! Return 404 if deleted is return 0, which means there is no taste_note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Taste note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add Taste note",
        )
