from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field


class AuditMixin(SQLModel):
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    deleted_at: Optional[datetime] | None = None