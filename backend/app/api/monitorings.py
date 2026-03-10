from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import ClassState, Monitoring, User
from app.schemas.monitoring import ClassStateResponse, MonitoringCreate, MonitoringResponse, MonitoringUpdate

router = APIRouter(prefix='/api/monitorings', tags=['monitorings'])


@router.get('', response_model=list[MonitoringResponse])
def list_monitorings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[MonitoringResponse]:
    monitorings = db.scalars(select(Monitoring).where(Monitoring.user_id == current_user.id).order_by(desc(Monitoring.created_at))).all()
    response = []
    for item in monitorings:
        last_state = db.scalar(
            select(ClassState).where(ClassState.monitoring_id == item.id).order_by(desc(ClassState.observed_at)).limit(1)
        )
        response.append(
            MonitoringResponse(
                id=item.id,
                discipline_code=item.discipline_code,
                discipline_name=item.discipline_name,
                class_group=item.class_group,
                semester=item.semester,
                check_interval_seconds=item.check_interval_seconds,
                active=item.active,
                last_state=ClassStateResponse.model_validate(last_state).model_dump() if last_state else None,
            )
        )
    return response


@router.post('', response_model=MonitoringResponse)
def create_monitoring(payload: MonitoringCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> MonitoringResponse:
    monitoring = Monitoring(user_id=current_user.id, **payload.model_dump())
    db.add(monitoring)
    db.commit()
    db.refresh(monitoring)
    return MonitoringResponse.model_validate(monitoring)


@router.patch('/{monitoring_id}', response_model=MonitoringResponse)
def update_monitoring(monitoring_id: int, payload: MonitoringUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> MonitoringResponse:
    monitoring = db.get(Monitoring, monitoring_id)
    if not monitoring or monitoring.user_id != current_user.id:
        raise HTTPException(status_code=404, detail='Monitoramento não encontrado')
    monitoring.active = payload.active
    db.commit()
    db.refresh(monitoring)
    return MonitoringResponse.model_validate(monitoring)


@router.delete('/{monitoring_id}', status_code=204)
def delete_monitoring(monitoring_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    monitoring = db.get(Monitoring, monitoring_id)
    if not monitoring or monitoring.user_id != current_user.id:
        raise HTTPException(status_code=404, detail='Monitoramento não encontrado')
    db.delete(monitoring)
    db.commit()


@router.get('/{monitoring_id}/history', response_model=list[ClassStateResponse])
def monitoring_history(monitoring_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ClassStateResponse]:
    monitoring = db.get(Monitoring, monitoring_id)
    if not monitoring or monitoring.user_id != current_user.id:
        raise HTTPException(status_code=404, detail='Monitoramento não encontrado')
    states = db.scalars(select(ClassState).where(ClassState.monitoring_id == monitoring_id).order_by(desc(ClassState.observed_at)).limit(100)).all()
    return [ClassStateResponse.model_validate(state) for state in states]
