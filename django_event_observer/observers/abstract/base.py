__all__ = ("BaseAbstractObserver",)

from abc import ABC, abstractmethod

from ...events.base import BaseEvent


class BaseAbstractObserver(ABC):
    @abstractmethod
    def update(self, event: BaseEvent) -> None: ...
