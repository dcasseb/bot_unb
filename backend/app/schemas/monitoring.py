from datetime import datetime

from pydantic import BaseModel, HttpUrl


class MonitoringCreate(BaseModel):
    discipline_code: str
    discipline_name: str | None = None
    class_group: str
    semester: str
    check_interval_seconds: int = 120
    query_url: HttpUrl


class MonitoringUpdate(BaseModel):
    active: bool


class MonitoringResponse(BaseModel):
    id: int
    discipline_code: str
    discipline_name: str | None
    class_group: str
    semester: str
    check_interval_seconds: int
    active: bool
    last_state: dict | None = None

    class Config:
        from_attributes = True


class ClassStateResponse(BaseModel):
    id: int
    total_seats: int | None
    occupied_seats: int | None
    available_seats: int | None
    status: str | None
    observed_at: datetime

    class Config:
        from_attributes = True
