from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)

@router.get("/", response_model=List[schemas.Driver])
def get_drivers(db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()
    return drivers

@router.put("/{id}", response_model=schemas.Driver)
def update_driver(id: int,
                updated_driver: schemas.DriverUpdateProgress,
                db: Session = Depends(get_db)):
    driver_query = db.query(models.Driver).filter(models.Driver.id == id)
    driver = driver_query.first()
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Driver with id: {id} does not found")
    driver_query.update(updated_driver.dict(), synchronize_session=False)
    db.commit()
    return driver_query.first()