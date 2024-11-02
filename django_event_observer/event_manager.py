from __future__ import annotations


__all__ = ("EventManager",)


from collections import defaultdict
import typing

from .events.base import BaseEvent  # noqa: TCH001
from .observers.abstract import BaseAbstractObserver


_ObserversT = typing.Dict[str, typing.List[BaseAbstractObserver]]  # noqa: UP006


class EventManager:
    _instance = None
    _subscriptions: typing.ClassVar[_ObserversT] = defaultdict(list)

    def subscribe(self, event_type: str, observer: BaseAbstractObserver) -> None:
        self._subscriptions[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer: BaseAbstractObserver) -> None:
        self._subscriptions[event_type].remove(observer)

    def notify(self, event: BaseEvent) -> None:
        for observer in self._subscriptions[event.event_type]:
            observer.update(event)
