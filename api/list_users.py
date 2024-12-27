from fastapi import Depends, APIRouter

from db import default_db
from models import User
from repositories.default.users import UsersRepository
from schemas import UserSchema

router = APIRouter()


class ListUsersRepository(UsersRepository):
    async def list_users(self):
        order_by = (User.first_name,)
        return await self.all(order_by=order_by)


@router.get("/users", response_model=list[UserSchema])
@default_db.init_session()
async def list_users(repo: ListUsersRepository = Depends()):
    return await repo.list_users()
