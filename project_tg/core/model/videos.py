from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, Integer, func

from core.model import BaseDB
from core.model.mixins import IdPrKey

if TYPE_CHECKING:
    from .video_snapshots import VideoSnapshots


class Video(BaseDB, IdPrKey):
    creator_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    video_created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comments_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reports_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    snapshots: Mapped[list["VideoSnapshots"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan",
    )
