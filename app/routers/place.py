from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/places",
    tags=["Places"]
)


@router.get("/", response_model=List[schemas.Place])
def get_places(db: Session = Depends(get_db)):
    places = db.query(models.Place).all()
    return places