from sqlalchemy import UniqueConstraint, BigInteger, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy_utils import URLType

from common.ORM.database import Base, Session
from common.ORM.mixins.fields import TimestampMixin, IDMixin
from .schemas import SubscriptionCreateModel, SubscriptionModel
from ..exceptions import AlreadyExistsError


class Subscription(Base,
                   TimestampMixin, IDMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (
        UniqueConstraint('telegram_id', 'url', name='_telegram_id_url_uc'),
    )

    url = mapped_column(URLType(), nullable=False)
    name: Mapped[str]
    telegram_id = mapped_column(BigInteger())
    frequency: Mapped[int] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    @validates("frequency")
    def validate_frequency(self,
                           _: str,
                           frequency: int):
        if frequency < 30:
            raise ValueError("frequency must be greater or equal 30 seconds")
        return frequency

    @classmethod
    async def get_all_user_subscriptions(cls,
                                         telegram_id: int,
                                         session: AsyncSession):
        q = select(cls).filter(
            cls.telegram_id == telegram_id
        )
        result = await session.execute(q)
        user_subs = result.scalars().all()
        return [SubscriptionModel.model_validate(user_sub) for user_sub in user_subs]

    @classmethod
    async def deactivate_user(cls,
                              telegram_id: int,
                              session: AsyncSession):
        q = update(cls).where(
            cls.telegram_id == telegram_id
        ).values(
            is_active=False
        )
        await session.execute(q)
        await session.commit()

    @classmethod
    async def get(cls,
                  sub_id: int,
                  session: AsyncSession):
        q = select(cls).filter(
            cls.id == sub_id
        )
        result = await session.execute(q)
        sub = result.scalars().one()
        sub_model = SubscriptionModel.model_validate(sub)
        return sub_model

    @classmethod
    async def get_all_active(cls):
        async with Session() as session:
            q = select(cls).filter_by(
                is_active=True
            )
            res = await session.execute(q)
            subs = res.scalars().all()
            return [SubscriptionModel.model_validate(sub) for sub in subs]

    async def check_exist(self, session: AsyncSession):
        q = select(
            select(type(self)).filter_by(
                telegram_id=self.telegram_id,
                url=self.url,
            ).exists()
        )
        res = await session.execute(q)
        return res.scalar()

    @classmethod
    async def add(cls,
                  sub_model: SubscriptionCreateModel,
                  session: AsyncSession):
        sub = cls(**sub_model.model_dump(mode="json"))
        is_exist = await sub.check_exist(session)
        if is_exist:
            raise AlreadyExistsError(f"Подписка {sub.url} уже существует.")

        session.add(sub)
        await session.commit()
        await session.refresh(sub)
        return SubscriptionModel.model_validate(sub)

    @classmethod
    async def delete(cls,
                     sub_id: int,
                     session: AsyncSession):
        q = delete(cls).filter(
            cls.id == sub_id
        )
        await session.execute(q)
        await session.commit()

    @classmethod
    async def set_is_active(cls,
                            sub_id: int,
                            is_active: bool,
                            session: AsyncSession):
        q = update(cls).where(
            cls.id == sub_id
        ).values(
            is_active=is_active
        )

        await session.execute(q)
        await session.commit()

    @classmethod
    async def update_name(cls,
                          sub_id: int,
                          name: str,
                          session: AsyncSession):
        q = update(cls).where(
            cls.id == sub_id
        ).values(
            name=name
        )
        await session.execute(q)
        await session.commit()

    @classmethod
    async def update_frequency(cls,
                               sub_id: int,
                               frequency: int,
                               session: AsyncSession):
        q = update(cls).where(
            cls.id == sub_id
        ).values(
            frequency=frequency
        )
        await session.execute(q)
        await session.commit()
