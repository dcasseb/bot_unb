from celery import Celery
from sqlalchemy import desc, select

import httpx

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.models import ClassState, Monitoring, Notification, NotificationType
from app.services.sigaa import parse_sigaa_class_status

settings = get_settings()
celery_app = Celery('monitor_worker', broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    'scan-monitorings-every-minute': {
        'task': 'app.workers.celery_app.scan_monitorings',
        'schedule': 60.0,
    }
}


def _send_telegram_message(message: str) -> bool:
    if not (
        settings.telegram_notifications_enabled
        and settings.telegram_bot_token
        and settings.telegram_chat_id
    ):
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {'chat_id': settings.telegram_chat_id, 'text': message}

    try:
        resp = httpx.post(url, data=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception:
        return False


@celery_app.task(name='app.workers.celery_app.scan_monitorings')
def scan_monitorings() -> None:
    with SessionLocal() as db:
        monitorings = db.scalars(select(Monitoring).where(Monitoring.active.is_(True))).all()
        for monitoring in monitorings:
            try:
                resp = httpx.get(monitoring.query_url, timeout=20)
                resp.raise_for_status()
            except Exception:
                continue

            parsed = parse_sigaa_class_status(resp.text)
            new_state = ClassState(
                monitoring_id=monitoring.id,
                total_seats=parsed['total_seats'],
                occupied_seats=parsed['occupied_seats'],
                available_seats=parsed['available_seats'],
                status=parsed['status'],
            )
            db.add(new_state)

            prev = db.scalar(
                select(ClassState)
                .where(ClassState.monitoring_id == monitoring.id)
                .order_by(desc(ClassState.observed_at))
                .offset(1)
                .limit(1)
            )
            if prev and prev.available_seats != new_state.available_seats:
                message = (
                    f'[{monitoring.discipline_code}-{monitoring.class_group}] '
                    f'Vagas: {prev.available_seats} -> {new_state.available_seats}'
                )

                db.add(
                    Notification(
                        user_id=monitoring.user_id,
                        type=NotificationType.browser,
                        message=message,
                        sent=False,
                    )
                )

                if (prev.available_seats or 0) < (new_state.available_seats or 0):
                    telegram_sent = _send_telegram_message(message)
                    db.add(
                        Notification(
                            user_id=monitoring.user_id,
                            type=NotificationType.telegram,
                            message=message,
                            sent=telegram_sent,
                        )
                    )
        db.commit()
