from fastapi import Depends, APIRouter
from pydantic import BaseModel

from db import default_db
from repositories.default.users import UsersRepository
from schemas import UserSchema

router = APIRouter()


class InputData(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


@router.patch("/user/{user_id}", response_model=UserSchema)
@default_db.init_session()
async def get_user(user_id: int, data: InputData, repo: UsersRepository = Depends()):
    user = await repo.get_by_pk(user_id)
    return await repo.update(instance=user, values=data.model_dump(exclude_unset=True))
