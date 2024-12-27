from sqlalchemy import MetaData, URL, make_url

from external_lib_emulation.db import Database

metadata = MetaData()

# print(make_url("postgresql+asyncpg://postgres:postgres@localhost:5433/postgres"))
default_db = Database("postgresql+asyncpg://postgres:postgres@localhost:5433/postgres")
# org_structure_db = Database("jdbc:postgresql+asyncpg://localhost:5433/org-structure-db")
