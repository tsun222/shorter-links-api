import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any
from datetime import datetime, timezone
from .extensions import db

class Url(db.Model):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    url: Mapped[str] = mapped_column(sa.String(2048), nullable=False)
    short_code: Mapped[str] = mapped_column(sa.String(8), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    access_count: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "url": self.url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_statistics(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "url": self.url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "access_count": self.access_count
        }