import functools
import logging
from contextvars import ContextVar
from functools import wraps

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, AsyncTransaction, AsyncConnection

session_context = ContextVar("session")

logger = logging.getLogger("db")
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class SessionNotInitializedError(Exception):

    def __init__(self):
        super().__init__("Сессия не проинициализована")


class Session:
    """
    Обертка над сессией алхимии.
    Создает сессию, кладет ее в contextvars, предоставляет возможности для управления ее жизненным циклом
    как в форме декоратора, так и в форме контекстного менеджера
    Сессия либо будет с autocommit, либо во внешней транзакции
    """
    def __init__(self, bind: AsyncEngine | AsyncConnection):
        self.bind = bind
        self.token = None

    async def __aenter__(self):
        self.session = AsyncSession(bind=self.bind, expire_on_commit=False)
        self.token = session_context.set(self.session)
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        await self.session.close()
        session_context.reset(self.token)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with self:
                return await func(*args, **kwargs)

        return wrapper


class Transaction:
    """
    Обертка над транзакцией алхимии.
    """

    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        self.session = None

    async def __aenter__(self):
        connection = await self.engine.connect()
        self.transaction = await connection.begin()
        self.session = Session(bind=connection)
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.session.__aexit__()

    def __call__(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with self:
                return await func(*args, **kwargs)

        return wrapper  # type: ignore

    async def commit(self):
        await self.transaction.commit()

    async def rollback(self):
        await self.transaction.rollback()


class Database:
    """
    Класс для взаимодействия с БД
    По факту предназначена для взаимодействия с сессией.  Можно рассматривать это как обертку над сессией алхимии
    Сессия находится на защищенной проперти __session, чтобы ее нельзя было использовать напрямую
    """
    def __init__(self, url):
        self.engine = create_async_engine(url, echo=True)

    def init_session(self):
        """
        Инициализирует сессию.
        Перед работой с БД нужно вызвать этот метод или метод transaction.

        Можно применять в виде декоратора (например, обернуть вьюху):

        @router.get("/user/{user_id}", response_model=UserSchema)
        @default_db.init_session()
        async def get_user(user_id: int, repo: UsersRepository = Depends()):
            return await repo.get_by_pk(user_id)

        или в виде контекстного менеджера (например, где-нибудь в таске faststream):

        async with default_db.init_session():
            repo = UsersRepository()
            await repo.get_by_pk(1)

        """
        return Session(self.engine.execution_options(isolation_level="AUTOCOMMIT"))

    @property
    def __session(self) -> AsyncSession:
        # возвращает текущую сессию из контекста
        # поэтому если работать с БД только через этот класс, то можно быть уверенным, что всегда будет только одна сессия
        # todo: стоит ли так жестить с недоступностью объекта сессии?
        try:
            return session_context.get()
        except LookupError:
            raise SessionNotInitializedError

    def transaction(self):
        """
        Инициализирует сессию (помещает в contextvars), которая при этом находится во внешней транзакции.
        Перед работой с БД нужно вызвать этот метод или метод init_session.

        Можно использовать в виде декортатора (например, обернуть вьюху):

        @router.post("/user-raise", response_model=UserSchema)
        @default_db.transaction()
        async def create_user(data: InputData, repo: UsersRepository = Depends()):
            user = await repo.create(**data.model_dump())
            # созданная запись будет откачена благодаря транзакции
            raise
            return user

        или в виде контекстного менеджера (например, где-нибудь в таске faststream):

        async with default_db.transaction():
            repo = UsersRepository()
            user = await repo.create(**data.model_dump())
            # созданная запись будет откачена благодаря транзакции
            raise

        """
        return Transaction(self.engine)

    # оберточные методы к методами сессии

    async def scalar(self, statement):
        return await self.__session.scalar(statement)

    async def scalars(self, statement):
        return await self.__session.scalars(statement)

    async def execute(self, statement):
        return await self.__session.execute(statement)

    async def get_by_pk(self, entity, ident, **kwargs):
        return await self.__session.get(entity, ident, **kwargs)
