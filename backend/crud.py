from typing import List
from fastapi.routing import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api")
