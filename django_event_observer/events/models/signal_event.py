from __future__ import annotations


__all__ = ("BaseModelSignalEvent",)

from django.db import models

from ..base import BaseEvent
from .model_event_enums import ModelSignalEventEnum  # noqa: TCH001


class BaseModelSignalEvent(BaseEvent[models.Model]):
    def __init__(self, signal_name: ModelSignalEventEnum, instance: models.Model):
        self.signal_name = signal_name
        self.model_type = type(instance)
        super().__init__("model_signal", instance)

    def __str__(self):
        return f"{self.event_data}:{self.event_type}{self.signal_name}"
