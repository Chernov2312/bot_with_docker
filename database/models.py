from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Plans(Base):
    __tablename__ = 'plans'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plans:Mapped[String] = mapped_column(String(250), nullable= False)