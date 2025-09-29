from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/", response_model=List[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

@router.get("/{id}", response_model=schemas.Item)
def get_item(id: int,
              db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} was not found")
    return item