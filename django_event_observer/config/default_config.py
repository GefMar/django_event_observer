__all__ = ("DJANGO_EVENT_OBSERVER",)

from types import MappingProxyType


DJANGO_EVENT_OBSERVER = MappingProxyType(
    {
        "EVENT_MANAGER": "django_event_observer.event_manager.EventManager",
        "AUTO_OBSERVERS": [],
    }
)
