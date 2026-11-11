from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError


from app.database import get_db
from app.schemas import ObjectCreate, ObjectGet, ObjectUpdate
from app.crud import read_object, update_object, read_objects
from app.crud import create_object
from app.crud import delete_object
from app.database import Base, engine
from app.auth import require_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, dependencies=[Depends(require_api_key)])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "OK"}


@app.post(
    path="/objects", response_model=ObjectGet, status_code=status.HTTP_201_CREATED
)
def post_object(payload: ObjectCreate, session=Depends(get_db)) -> ObjectGet:
    try:
        record = create_object(session=session, payload=payload)
        result = ObjectGet.model_validate(record)
        return result
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Bad request, integrity error occured, check your input please",
        )


@app.get(path="/objects/{id}", response_model=ObjectGet, status_code=status.HTTP_200_OK)
def get_object(id: int, session=Depends(dependency=get_db)) -> ObjectGet:
    record = read_object(session=session, item_id=id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Object id: {id} - Not found")
    return ObjectGet.model_validate(record)


@app.get(
    path="/objects", response_model=list[ObjectGet], status_code=status.HTTP_200_OK
)
def get_objects(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session=Depends(dependency=get_db),
) -> list[ObjectGet]:
    results = read_objects(session, limit, offset)
    return [ObjectGet.model_validate(result) for result in results]


@app.delete(path="/objects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_object(id: int, session=Depends(dependency=get_db)):
    if delete_object(session, id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object wasn't found"
        )


@app.patch(
    path="/objects/{id}", response_model=ObjectGet, status_code=status.HTTP_200_OK
)
def patch_object(id: int, payload: ObjectUpdate, session=Depends(dependency=get_db)):
    try:
        item = update_object(session, id, payload)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Bad request, integrity error occured, check your input please",
        )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No item found, no item updated",
        )
    return item
