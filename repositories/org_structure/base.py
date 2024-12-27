from db import org_structure_db
from external_lib_emulation.repositories.base import BaseRepository, ModelRepository


# базовый репозиторий для моделей БД приложения (дефолтной)
# при наличии одной БД в приложении можно назвать просто BaseRepository
class OrgStructureBaseRepository(BaseRepository):
    def __init__(self):
        super().__init__(org_structure_db)


# базовый модельный репозиторий для моделей БД приложения (дефолтной)
# при наличии одной БД в приложении можно назвать просто ModelRepository
class OrgStructureModelRepository(ModelRepository):
    def __init__(self):
        super().__init__(org_structure_db)
