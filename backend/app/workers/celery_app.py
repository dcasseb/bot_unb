from celery import Celery
from sqlalchemy import desc, select

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.models import ClassState, Monitoring, Notification, NotificationType
from app.services.sigaa import parse_sigaa_class_status

import httpx

settings = get_settings()
celery_app = Celery('monitor_worker', broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.beat_schedule = {
    'scan-monitorings-every-minute': {
        'task': 'app.workers.celery_app.scan_monitorings',
        'schedule': 60.0,
    }
}


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
                db.add(
                    Notification(
                        user_id=monitoring.user_id,
                        type=NotificationType.browser,
                        message=(
                            f'[{monitoring.discipline_code}-{monitoring.class_group}] '
                            f'Vagas: {prev.available_seats} -> {new_state.available_seats}'
                        ),
                        sent=False,
                    )
                )
        db.commit()
