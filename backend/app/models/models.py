from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class NotificationType(str, Enum):
    telegram = 'telegram'
    email = 'email'
    browser = 'browser'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    monitorings: Mapped[list['Monitoring']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Monitoring(Base):
    __tablename__ = 'monitorings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    discipline_code: Mapped[str] = mapped_column(String(50), index=True)
    discipline_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    class_group: Mapped[str] = mapped_column(String(20))
    semester: Mapped[str] = mapped_column(String(20), index=True)
    check_interval_seconds: Mapped[int] = mapped_column(Integer, default=120)
    query_url: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='monitorings')
    states: Mapped[list['ClassState']] = relationship(back_populates='monitoring', cascade='all, delete-orphan')


class ClassState(Base):
    __tablename__ = 'class_states'

    id: Mapped[int] = mapped_column(primary_key=True)
    monitoring_id: Mapped[int] = mapped_column(ForeignKey('monitorings.id', ondelete='CASCADE'), index=True)
    total_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    occupied_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    available_seats: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str | None] = mapped_column(String(80), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    monitoring: Mapped['Monitoring'] = relationship(back_populates='states')


class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    type: Mapped[NotificationType] = mapped_column(SAEnum(NotificationType))
    message: Mapped[str] = mapped_column(Text)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
