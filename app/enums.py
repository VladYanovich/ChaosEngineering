from enum import Enum

class LocationType(str, Enum):
    factory = "factory"
    warehouse = "warehouse"

class StatusType(str, Enum):
    await_confirmation = "await confirmation"
    confirmed = "confirmed"
    in_delivery = "in delivery"
    delivered = "delivered"
    canceled = "canceled"

class DriverStatus(str, Enum):
    free = "free"
    enroute = "enroute"