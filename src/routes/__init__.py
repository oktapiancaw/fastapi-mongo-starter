from fastapi import APIRouter

from .api import bean, brew_method, event, note, person, store, taste_note, wiki
from .middleware import ProcessTimeAndLogMiddleware

router = APIRouter()
router.include_router(bean.app, prefix="/beans", tags=["Beans"])
router.include_router(
    brew_method.app, prefix="/brew/manual-methods", tags=["Brew Method"]
)
router.include_router(event.app, prefix="/event", tags=["Events"])
router.include_router(note.app, prefix="/note", tags=["Notes"])
router.include_router(person.app, prefix="/person", tags=["Persons"])
router.include_router(store.app, prefix="/store", tags=["Stores"])
router.include_router(wiki.app, prefix="/wiki", tags=["Wiki"])
router.include_router(taste_note.app, prefix="/taste-note", tags=["Taste Note"])
