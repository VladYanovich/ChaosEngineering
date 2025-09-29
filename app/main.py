from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db, engine
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy import text
from app.routers import order, driver, item, place


from fastapi import FastAPI

app = FastAPI()

app.include_router(order.router)
app.include_router(driver.router)
app.include_router(item.router)
app.include_router(place.router)

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.get("/health")
def healthcheck():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        print("FAIL-------------------")
        return {"status": "error", "database": str(e)}
