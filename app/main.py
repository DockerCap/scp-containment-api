from fastapi import FastAPI

from app.schemas import ObjectCreate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/visited/{id}")
async def visited(id: str):
    return {"message": f"Bro visited his {id}"}

@app.post("/try-schema")
async def try_schema(payload: ObjectCreate):
    return payload