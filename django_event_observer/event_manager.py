__all__ = ("EventManager",)

from collections import defaultdict
import typing

from .events.base import BaseEvent
from .observers.abstract import BaseAbstractObserver


_ObserversT = dict[str, list[BaseAbstractObserver]]


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
