from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.enums import LocationType, StatusType, DriverStatus


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    from_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    to_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    status_id = Column(Integer, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=True)

    @property
    def product(self):
        return self.item.product if self.item else None

    @property
    def status(self):
        return self.status_rel.type if self.status_rel else None

    driver = relationship("Driver", back_populates="orders")
    item = relationship("Item")
    from_place = relationship("Place", foreign_keys=[from_id])
    to_place = relationship("Place", foreign_keys=[to_id])
    status_rel = relationship("Status")


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, nullable=False)
    street_name = Column(String, nullable=False)
    type = Column(Enum(LocationType), nullable=False)


class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(StatusType), nullable=False)


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    progress = Column(Integer, nullable=True)
    est_delivery_time = Column(Integer, nullable=True)
    driverstatus_id = Column(Integer, ForeignKey("driver_statuses.id", ondelete="CASCADE"), nullable=False)

    orders = relationship("Order", back_populates="driver")


class DriverStatus(Base):
    __tablename__ = "driver_statuses"
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Enum(DriverStatus), nullable=False)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False)
    product = Column(String, nullable=False)
    description = Column(String, nullable=True)


class PlaceItem(Base):
    __tablename__ = "place_items"
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), primary_key=True)
    amount = Column(Integer, nullable=False)


class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    previous_status_id = Column(Integer, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)
    new_status_id = Column(Integer, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))