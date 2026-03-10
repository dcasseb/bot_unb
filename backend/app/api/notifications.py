from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Notification, User
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix='/api/notifications', tags=['notifications'])


@router.get('', response_model=list[NotificationResponse])
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[NotificationResponse]:
    items = db.scalars(
        select(Notification).where(Notification.user_id == current_user.id).order_by(desc(Notification.created_at)).limit(100)
    ).all()
    return [NotificationResponse.model_validate(item) for item in items]
