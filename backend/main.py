from typing import Union
from sqlalchemy.orm import Session
import db.models as models
from fastapi import FastAPI, Depends
from config import get_settings

app = FastAPI()

print(f"Test : {get_settings().database_url}")

# @app.get("/")
# def read_root(db: Session = Depends(get_db)):
#     pass


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
