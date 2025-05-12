from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from leafsource.config import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    isbn: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    copies_available: Mapped[int] = mapped_column(Integer, default=1)

    # relationship to borrow records
    borrows = relationship("Borrow", back_populates="book")