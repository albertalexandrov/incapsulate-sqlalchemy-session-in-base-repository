from fastapi import Depends, APIRouter

from db import default_db
from repositories.default.users import UsersRepository
from schemas import UserSchema

router = APIRouter()


@router.get("/user/{user_id}", response_model=UserSchema)
@default_db.init_session()
async def get_user(user_id: int, repo: UsersRepository = Depends()):
    return await repo.get_by_pk(user_id)
