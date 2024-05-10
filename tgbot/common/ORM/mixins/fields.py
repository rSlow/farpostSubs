from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class IDMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    edited_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        nullable=True
    )


class ModelNameMixin:
    @declared_attr
    def __tablename__(self):
        if self.__tablename__:
            return self.__tablename__
        class_name = self.__class__.__name__
        return class_name.lower()
