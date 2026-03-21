from app.models.user import User
from app.repositories.abstract_repository import AbstractRepository
from typing import override


class UserRepository(AbstractRepository[User]):

    @override
    def create(self, entity: User) -> User:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> User | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[User]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError