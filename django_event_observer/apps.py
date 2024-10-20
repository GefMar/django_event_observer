from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

from .config import default_config
from .event_manager import EventManager
from .observers.abstract import BaseAbstractObserver


class DjangoEventObserverConfig(AppConfig):
    _event_manager: EventManager | None = None
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_event_observer"

    @property
    def app_settings(self):
        result = default_config.DJANGO_EVENT_OBSERVER.copy()
        if isinstance(getattr(settings, "DJANGO_EVENT_OBSERVER", None), dict):
            result.update(settings.DJANGO_EVENT_OBSERVER)
        return result

    @property
    def event_manager(self):
        if self._event_manager is None:
            msg = f"{self.__class__.__name__} is not Ready"
            raise ValueError(msg)
        return self._event_manager

    def load_event_manager(self) -> EventManager:
        event_manager_class = import_string(self.app_settings["EVENT_MANAGER"])
        if not issubclass(event_manager_class, EventManager):
            msg = f"{event_manager_class} is not a subclass of EventManager"
            raise TypeError(msg)
        return event_manager_class()

    def ready(self):
        self.load_event_manager()
        self._auto_subscribe_observers()

    def _auto_subscribe_observers(self):
        for auto_observer in self.app_settings.get("AUTO_OBSERVERS", []):
            observer_cls = import_string(auto_observer.get("CLASS"))
            if not issubclass(observer_cls, BaseAbstractObserver):
                msg = f"{observer_cls} is not a subclass of BaseAbstractObserver"
                raise TypeError(msg)
            observer = import_string(auto_observer["CLASS"])(
                *auto_observer.get("INIT_ARGS", []), **auto_observer.get("INIT_KWARGS", {})
            )
            for event_type in auto_observer.get("EVENT_TYPES", []):
                self.event_manager.subscribe(event_type, observer)
