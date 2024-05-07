from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class RetrieveMixin:
    @classmethod
    async def get(cls,
                  session: AsyncSession,
                  value: Any,
                  filter_field: str = "id"):
        q = select(cls).filter(filter_field == value)
        result = await session.execute(q)
        obj = result.scalars().one_or_none()
        return obj


class UpdateMixin:
    @classmethod
    async def update(cls,
                     session: AsyncSession,
                     value: Any,
                     filter_field: str = "id"):
        q = update(cls).filter(filter_field == value)
        result = await session.execute(q)
        await session.commit()
        obj = result.scalars().one_or_none()
        return obj


class DeleteMixin:
    @classmethod
    async def delete(cls,
                     session: AsyncSession,
                     value: Any,
                     filter_field: str = "id"):
        q = delete(cls).filter(filter_field == value)
        await session.execute(q)
        await session.commit()
