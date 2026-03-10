from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    type: str
    message: str
    sent: bool
    created_at: datetime

    class Config:
        from_attributes = True
