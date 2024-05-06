from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


class Base(DeclarativeBase):
    pass


Engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)
Session = async_sessionmaker(
    bind=Engine,
    expire_on_commit=False,
    autoflush=True
)
