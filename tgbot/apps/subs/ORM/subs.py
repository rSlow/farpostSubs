from sqlalchemy import UniqueConstraint, BigInteger, select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import URLType

from apps.subs.ORM.schemas import SubscriptionCreateModel, SubscriptionModel
from common.ORM.database import Base
from common.ORM.mixins.crud import RetrieveMixin, UpdateMixin, DeleteMixin

from common.ORM.mixins.fields import TimestampMixin, IDMixin


class Subscription(Base,
                   TimestampMixin, IDMixin,
                   RetrieveMixin, UpdateMixin, DeleteMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint('telegram_id', 'url', name='_telegram_id_url_uc'),
    )

    url = mapped_column(URLType())
    _name = mapped_column(String(), nullable=True)
    telegram_id = mapped_column(BigInteger())
    frequency: Mapped[int] = mapped_column(default=1)  # in minutes
    is_active: Mapped[bool] = mapped_column(default=True)

    @hybrid_property
    def name(self):
        if not self._name:
            return self.url
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @classmethod
    async def get_from_user(cls,
                            telegram_id: int,
                            session: AsyncSession):
        q = select(cls).filter(
            cls.telegram_id == telegram_id
        )
        result = await session.execute(q)
        user_subs = result.scalars().all()
        return user_subs

    @classmethod
    async def add(cls,
                  sub_model: SubscriptionCreateModel,
                  session: AsyncSession):
        sub = cls(**sub_model.model_dump())
        session.add(sub)
        await session.commit()
        await session.refresh(sub)
        return SubscriptionModel.model_validate(sub)
