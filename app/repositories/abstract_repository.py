from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[T]:
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        pass
