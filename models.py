from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db import metadata


class Base(DeclarativeBase):
    metadata = metadata


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]

    def __str__(self):
        return f"{self.__class__.__name__}{{id={self.id}, first_name={self.first_name}, last_name={self.last_name}}}"
