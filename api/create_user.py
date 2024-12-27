from fastapi import APIRouter, Depends
from pydantic import BaseModel

from db import default_db
from repositories.default.users import UsersRepository
from schemas import UserSchema

router = APIRouter()


class InputData(BaseModel):
    first_name: str
    last_name: str


@router.post("/user", response_model=UserSchema)
@default_db.init_session()
async def create_user(data: InputData, repo: UsersRepository = Depends()):
    user = await repo.create(**data.model_dump())
    print("Создан пользователь", user)
    return user
