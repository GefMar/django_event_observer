from __future__ import annotations


__all__ = ("BaseEvent",)

import typing

from django.apps import apps


if typing.TYPE_CHECKING:
    from ..event_manager import EventManager


_EventDataT = typing.TypeVar("_EventDataT")


class BaseEvent(typing.Generic[_EventDataT]):
    def __init__(self, event_type: str, event_data: _EventDataT):
        self._event_manager: EventManager = apps.get_app_config("django_event_observer").event_manager
        self.event_type = event_type
        self.event_data = event_data

    def __call__(self):
        self.notify()

    def notify(self):
        self._event_manager.notify(self)

    def __str__(self):
        return f"{self.event_data}:{self.event_type}"
