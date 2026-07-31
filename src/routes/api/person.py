from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.person import Person, Persons, PersonSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.person import PersonService

app = APIRouter()
service = PersonService("key-persons")


@app.get(
    "",
    name="Get all persons",
    responses={**ServiceResponse(Persons).multi("get_persons", obj="Person")},
)
def get_persons():
    try:
        # ? Get total of person, and the persons data
        count, persons = service.get_persons()

        # ? Check if persons is not empty
        if persons:
            # * Return 200 if persons is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all persons",
                    "total": count,
                    "data": persons.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if persons is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Persons not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all person",
        )


@app.post(
    "/search",
    name="Get all persons",
    responses={**ServiceResponse(Persons).multi("get_persons", obj="Person")},
)
def search_persons(payload: SearchSchema):
    try:
        # ? Get total of person, and the persons data
        count, persons = service.search_persons(payload)

        # ? Check if persons is not empty
        if persons:
            # * Return 200 if persons is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all persons",
                    "total": count,
                    "data": persons.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if persons is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Persons not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all person",
        )


@app.get(
    "/{id}",
    responses={**ServiceResponse(Person).get("get_person", obj="Person")},
)
def get_person(id: str = Path(..., description="Person id")):
    try:
        # ? Check if person is not empty
        if person := service.get_person(id):
            # * Return 200 if persons is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": person.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if person is empty, which means there is no person with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Person not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get person",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Person).creation("add_person", obj="Person")},
)
def add_person(data: PersonSchema):
    try:
        person = service.add_person(data)

        # * Return 201, and the person
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Person created successfully",
                "data": person.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add person",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Person).update("update_person", obj="Person")},
)
def update_person(
    data: PersonSchema, id: str = Path(..., description="Person id")
):
    try:
        # ? Check if person is updated successfully
        if service.update_person(id, data):
            # * Return 200, and id of the person
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Person updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no person with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Person not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add person",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Person).delete("delete_person", obj="Person")},
)
def delete_person(id: str = Path(..., description="Person id")):
    try:
        # ? Check if person is deleted successfully
        if service.delete_person(id):
            # * Return 200, and id of the person
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Person deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no person with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Person not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add person",
        )
