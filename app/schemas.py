from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Driver(BaseModel):
    name: str
    phone: str
    longitude: float
    latitude: float
    progress: Optional[int] = None
    est_delivery_time: Optional[int] = None

    class Config:
        from_attributes = True

class DriverUpdateProgress(BaseModel):
    progress: int

class Item(BaseModel):
    id: int
    product: str
    description: str

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    title: str
    product: str
    amount: int
    from_id: int
    to_id: int
    status: Optional[str] = None
    created_at: datetime
    driver: Driver
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    title: str
    item_id: int
    amount: int
    from_id: int
    to_id: int
    status_id: int
    driver_id: Optional[int] = None

class Place(BaseModel):
    id: int
    street_name: str
    type: str