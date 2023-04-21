from typing import Union
from database import engine
from fastapi import FastAPI

app = FastAPI()


with engine.connect() as connection:
    print(connection)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
