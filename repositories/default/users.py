from models import User
from repositories.default.base import DefaultModelRepository


class UsersRepository(DefaultModelRepository):
    model = User
