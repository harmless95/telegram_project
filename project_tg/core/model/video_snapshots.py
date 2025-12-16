from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, TIMESTAMP, func

from core.model import BaseDB
from core.model.mixins import IdPrKey

if TYPE_CHECKING:
    from .videos import Video


class VideoSnapshots(BaseDB, IdPrKey):
    video_id: Mapped[UUID] = mapped_column(ForeignKey("videos.id"), nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reports_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    delta_views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    delta_likes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    delta_comments_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    delta_reports_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    video: Mapped["Video"] = relationship(back_populates="snapshots")
