from sqlalchemy import select, inspect, update
from sqlalchemy.dialects.postgresql import insert

from external_lib_emulation.db import Database


class BaseRepository:
    """
    Базовый репозиторий для базового модельного репозитория, а также для сервисных репозиториев
    """

    def __init__(self, db: Database):
        self._db = db

    async def scalar(self, statement):
        # метод-shortcut
        return await self._db.scalar(statement)

    async def scalars(self, statement):
        # метод-shortcut
        return await self._db.scalars(statement)

    async def execute(self, statement):
        # метод-shortcut
        return await self._db.execute(statement)

    # какие-то другие методы базового репозитория, типа count


class ModelRepository(BaseRepository):
    """
    Базовый модельный базовый репозиторий.
    """
    model = None

    def __init__(self, db: Database):
        if not self.model:
            raise ValueError(f"В атрибуте {self.__class__.__name__}.model не определена модель")
        super().__init__(db)

    async def get_by_pk(self, pk, options=()):
        return await self._db.get_by_pk(self.model, pk, options=options)

    async def create(self, **values: dict):
        stmt = insert(self.model).values(**values)
        return await self.scalar(stmt)

    async def update(self, *, values: dict, instance=None):
        # функциональность будет планируется расширять, чтобы мочь обновлять массово
        inspection_obj = inspect(instance)
        whereclause = [k == v for k, v in zip(inspection_obj.mapper.primary_key, inspection_obj.identity)]
        stmt = update(self.model).where(*whereclause).values(**values).returning(self.model)
        await self.scalar(stmt)  # можно не присваивать, алхимия обновить instance
        return instance

    async def all(self, order_by=(), options=()):
        statement = select(self.model).order_by(*order_by).options(*options)
        return (await self.scalars(statement)).all()

    async def bulk_create(self, values: list[dict]):
        stmt = insert(self.model).values(values).returning(self.model)
        return await self.scalars(stmt)

    # какие-то другие методы модельного репо
