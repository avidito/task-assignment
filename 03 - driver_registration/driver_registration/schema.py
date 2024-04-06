from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime


class DriverRegistration(BaseModel):
    id: str
    date_created: datetime
    date_last_modified: datetime
    active_date: datetime
    name: str
    phone: str
    resign_date: Optional[datetime] = None
    resign_reason: Optional[str] = None
    status: int
    tipe: int
    area: int
    operator: str
    modified_by: Optional[str] = None
    vehicle_type: str
    helmet_qty: Optional[str] = None
    jacket_qty: Optional[str] = None
    vehicle_brand: Optional[str] = None
    vehicle_year: Optional[str] = None
    bike_type: Optional[str] = None
    first_ride_bonus_awarded: Optional[bytes] = None
    is_doc_completed: Optional[bytes] = None

    @field_serializer('date_created')
    def serialize_date_created(self, date_created: datetime, _info):
        if (date_created):
            return date_created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    @field_serializer('date_last_modified')
    def serialize_date_last_modified(self, date_last_modified: datetime, _info):
        if (date_last_modified):
            return date_last_modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    @field_serializer('active_date')
    def serialize_active_date(self, active_date: datetime, _info):
        if (active_date):
            return active_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    @field_serializer('resign_date')
    def serialize_resign_date(self, resign_date: datetime, _info):
        if (resign_date):
            return resign_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    @field_serializer('first_ride_bonus_awarded')
    def serialize_first_ride_bonus_awarded(self, first_ride_bonus_awarded: bytes, _info):
        if (first_ride_bonus_awarded):
            return int.from_bytes(first_ride_bonus_awarded, "little")
    
    @field_serializer('is_doc_completed')
    def serialize_is_doc_completed(self, is_doc_completed: bytes, _info):
        if (is_doc_completed):
            return int.from_bytes(is_doc_completed, "little")
