from typing import Union
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from fastapi import FastAPI, Depends

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    types = db.query(models.Type).all()
    print(types)
    return types


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
