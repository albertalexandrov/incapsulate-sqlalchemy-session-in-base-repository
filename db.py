from sqlalchemy import MetaData, URL, make_url

from external_lib_emulation.db import Database

metadata = MetaData()

# подключение к дефолтной бд приложения (если бд одна, то можно назвать просто db)
default_db = Database("postgresql+asyncpg://postgres:postgres@localhost:5433/postgres")
# пример подключения, если в приложении несколько бд
# org_structure_db = Database("jdbc:postgresql+asyncpg://localhost:5433/org-structure-db")
