from sqlalchemy import (
    Integer,
    String,
    Float,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


# declarative base class
class Base(DeclarativeBase):
    pass


# assume all fields are nullable except for id
class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    discount_percentage: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    brand: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    thumbnail: Mapped[str] = mapped_column(String)


class ProductImage(Base):
    __tablename__ = "product_image"

    # id is set to autoincrement for simplicity
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(String)


class Cities(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    LatD: Mapped[int] = mapped_column(Integer)
    LatM: Mapped[int] = mapped_column(Integer)
    LatS: Mapped[int] = mapped_column(Integer)
    NS: Mapped[str] = mapped_column(String)
    LonD: Mapped[int] = mapped_column(Integer)
    LonM: Mapped[int] = mapped_column(Integer)
    LonS: Mapped[int] = mapped_column(Integer)
    EW: Mapped[str] = mapped_column(String)
    City: Mapped[str] = mapped_column(String)
    State: Mapped[str] = mapped_column(String)