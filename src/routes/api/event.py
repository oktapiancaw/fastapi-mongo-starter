from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.models.dto.event import Event, Events, EventSchema
from src.models.response import ServiceResponse
from src.models.schema import SearchSchema
from src.routes.services.event import EventService

app = APIRouter()
service = EventService("events")


@app.get(
    "",
    name="Get all events",
    responses={**ServiceResponse(Events).multi("get_events", obj="Event")},
)
def get_events():
    try:
        # ? Get total of event, and the events data
        count, events = service.get_events()

        # ? Check if events is not empty
        if events:
            # * Return 200 if events is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all events",
                    "total": count,
                    "data": events.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if events is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Events not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all event",
        )


@app.post(
    "/search",
    name="Get all events",
    responses={**ServiceResponse(Events).multi("get_events", obj="Event")},
)
def search_events(payload: SearchSchema):
    try:
        # ? Get total of event, and the events data
        count, events = service.search_events(payload)

        # ? Check if events is not empty
        if events:
            # * Return 200 if events is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success get all events",
                    "total": count,
                    "data": events.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if events is empty
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Events not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get all event",
        )


@app.get(
    "/{id}", responses={**ServiceResponse(Event).get("get_event", obj="Event")}
)
def get_event(id: str = Path(..., description="Event id")):
    try:
        # ? Check if event is not empty
        if event := service.get_event(id):
            # * Return 200 if events is not empty
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Success",
                    "data": event.model_dump(by_alias=True),
                },
            )

        # ! Return 404 if event is empty, which means there is no event with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Event not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed get event",
        )


@app.post(
    "",
    status_code=201,
    responses={**ServiceResponse(Event).creation("add_event", obj="Event")},
)
def add_event(data: EventSchema):
    try:
        event = service.add_event(data)

        # * Return 201, and the event
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Event created successfully",
                "data": event.model_dump(by_alias=True),
            },
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add event",
        )


@app.put(
    "/{id}",
    responses={**ServiceResponse(Event).update("update_event", obj="Event")},
)
def update_event(
    data: EventSchema, id: str = Path(..., description="Event id")
):
    try:
        # ? Check if event is updated successfully
        if service.update_event(id, data):
            # * Return 200, and id of the event
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Event updated successfully", "id": id},
            )

        # ! Return 404 if updated is return 0, which means there is no event with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Event not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add event",
        )


@app.delete(
    "/{id}",
    responses={**ServiceResponse(Event).delete("delete_event", obj="Event")},
)
def delete_event(id: str = Path(..., description="Event id")):
    try:
        # ? Check if event is deleted successfully
        if service.delete_event(id):
            # * Return 200, and id of the event
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"detail": "Event deleted successfully", "id": id},
            )

        # ! Return 404 if deleted is return 0, which means there is no event with the given id
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Event not found"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed add event",
        )
