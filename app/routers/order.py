from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@router.get("/{id}", response_model=schemas.Order)
def get_order(id: int,
              db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} was not found")
    return order

@router.put("/{id}", response_model=schemas.Order)
def update_post(id: int,
                updated_order: schemas.OrderCreate,
                db: Session = Depends(get_db)):
    order_query = db.query(models.Order).filter(models.Order.id == id)
    order = order_query.first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {id} does not found")
    order_query.update(updated_order.dict(), synchronize_session=False)
    db.commit()
    return order_query.first()