from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.note import Note, Notes, NoteSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.note import NoteService

app = APIRouter()
service = NoteService("notes")


@app.get(
    "",
    name="Get all notes",
    responses={**ServiceResponse(Notes).multi("get_notes", obj="Note")},
)
def get_notes():
    try:
        # ? Get total of note, and the notes data
        count, notes = service.get_notes()

        # ? Check if notes is not empty
        if notes:
            # * Return 200 if notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all notes",
                    "total": count,
                    "data": notes.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if notes is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Notes not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all note",
        )


@app.post(
    "/search",
    name="Get all notes",
    responses={**ServiceResponse(Notes).multi("get_notes", obj="Note")},
)
def search_notes(payload: SearchSchema):
    try:
        # ? Get total of note, and the notes data
        count, notes = service.search_notes(payload)

        # ? Check if notes is not empty
        if notes:
            # * Return 200 if notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all notes",
                    "total": count,
                    "data": notes.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if notes is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Notes not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all note",
        )


@app.get(
    "/{id}", responses={**ServiceResponse(Note).get("get_note", obj="Note")}
)
def get_note(id: str = Path(..., description="Note id")):
    try:
        # ? Check if note is not empty
        if note := service.get_note(id):
            # * Return 200 if notes is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": note.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if note is empty, which means there is no note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get note",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Note).creation("add_note", obj="Note")},
)
def add_note(data: NoteSchema):
    try:
        note = service.add_note(data)

        # * Return 201, and the note
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Note created successfully",
                "data": note.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add note",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Note).update("update_note", obj="Note")},
)
def update_note(data: NoteSchema, id: str = Path(..., description="Note id")):
    try:
        # ? Check if note is updated successfully
        if service.update_note(id, data):
            # * Return 200, and id of the note
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Note updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add note",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Note).delete("delete_note", obj="Note")},
)
def delete_note(id: str = Path(..., description="Note id")):
    try:
        # ? Check if note is deleted successfully
        if service.delete_note(id):
            # * Return 200, and id of the note
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Note deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no note with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Note not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add note",
        )
