from db import default_db
from external_lib_emulation.repositories.base import BaseRepository, ModelRepository


# базовый репозиторий для моделей БД приложения (дефолтной)
# при наличии одной БД в приложении можно назвать просто BaseRepository
class DefaultBaseRepository(BaseRepository):
    def __init__(self):
        super().__init__(default_db)


# базовый модельный репозиторий для моделей БД приложения (дефолтной)
# при наличии одной БД в приложении можно назвать просто ModelRepository
class DefaultModelRepository(ModelRepository):
    def __init__(self):
        super().__init__(default_db)
