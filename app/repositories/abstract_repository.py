from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def list_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
