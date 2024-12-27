from fastapi import Depends, APIRouter

from db import default_db
from repositories.default.users import UsersRepository
from schemas import UserSchema

router = APIRouter()


@router.get("/users/bulk", response_model=list[UserSchema])
@default_db.init_session()
async def bulk_create(repo: UsersRepository = Depends()):
    values = [{"first_name": "John", "last_name": "Snow"}, {"first_name": "Tirion", "last_name": "Lannister"}]
    return await repo.bulk_create(values)
