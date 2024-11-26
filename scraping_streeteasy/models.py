from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey, VARCHAR
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    listings: Mapped[list["Listing"]] = relationship(back_populates="url")

class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    prop_type: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    availability: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    amenity_feature: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    url_id: Mapped[int] = mapped_column(ForeignKey("urls.id"), nullable=False)
    url: Mapped["Url"] = relationship(back_populates="listings")