# django_event_observer


django_event_observer is a fully-fledged Django application designed for observing and handling events within your project. It provides a flexible and extensible framework for subscribing to various event types and reacting to them accordingly.

Installation

Install the package using pip:

pip install django_event_observer

Configuration

After installation, add django_event_observer to the INSTALLED_APPS in your Django settings file:

INSTALLED_APPS = [
    # ...
    'django_event_observer',
    # ...
]

Default Settings

By default, the DJANGO_EVENT_OBSERVER settings are as follows:

from types import MappingProxyType

DJANGO_EVENT_OBSERVER = MappingProxyType(
    {
        "EVENT_MANAGER": "django_event_observer.event_manager.EventManager",
        "AUTO_OBSERVERS": [],
    }
)

You can override the DJANGO_EVENT_OBSERVER variable in your project’s settings to specify a custom import path for the EventManager or to add automatic observers.

Customizing EventManager

If you need to use a custom EventManager, specify the import path in your settings:

DJANGO_EVENT_OBSERVER = {
    "EVENT_MANAGER": "my_app.event_manager.CustomEventManager",
    "AUTO_OBSERVERS": [],
}

Automatic Observers

The AUTO_OBSERVERS parameter is a list of dictionaries, each describing an observer. These observers are classes inheriting from django_event_observer.observers.abstract.base.BaseAbstractObserver.

Syntax:
```python


DJANGO_EVENT_OBSERVER = {
    "EVENT_MANAGER": "django_event_observer.event_manager.EventManager",
    "AUTO_OBSERVERS": [
        {
            "CLASS": "my_module.observers.MyObserver",
            "INIT_ARGS": ["arg1", "arg2"],
            "INIT_KWARGS": {"key1": "value1", "key2": "value2"},
            "EVENT_TYPES": ["event_type_1", "event_type_2"],
        },
        # Other observers...
    ],
}
```

	•	"CLASS": A string with the import path to the observer class.
	•	"INIT_ARGS": A list of positional arguments for class initialization.
	•	"INIT_KWARGS": A dictionary of keyword arguments for class initialization.
	•	"EVENT_TYPES": A list of strings representing event types that the observer should subscribe to.

##Usage

Creating a Custom Observer

To create a custom observer, inherit from BaseAbstractObserver and implement the update method:

# my_module/observers.py
```python


from django_event_observer.observers.abstract.base import BaseAbstractObserver
from django_event_observer.events.base import BaseEvent

class MyObserver(BaseAbstractObserver):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Additional initialization...

    def update(self, event: BaseEvent) -> None:
        # Logic to handle the event
        print(f"Received event: {event}")
```

Definition of BaseAbstractObserver:

# django_event_observer/observers/abstract/base.py

from abc import ABC, abstractmethod
from ...events.base import BaseEvent

class BaseAbstractObserver(ABC):
    @abstractmethod
    def update(self, event: BaseEvent) -> None:
        ...

Any custom observer must inherit from BaseAbstractObserver and implement the update method, which will be called when an event occurs.

Creating Custom Events

Events should inherit from BaseEvent and can use generics for typing event_data:

# my_module/events.py

from django_event_observer.events.base import BaseEvent
from typing import Generic, TypeVar

T = TypeVar('T')

class MyEvent(BaseEvent[T], Generic[T]):
    def __init__(self, event_type: str, event_data: T):
        super().__init__(event_type, event_data)
        # Additional initialization...

    def __str__(self):
        return f"{self.event_type}: {self.event_data}"

Definition of BaseEvent:

# django_event_observer/events/base.py

import typing
from django.apps import apps

if typing.TYPE_CHECKING:
    from ..event_manager import EventManager

_EventDataT = typing.TypeVar("_EventDataT")

class BaseEvent(typing.Generic[_EventDataT]):
    def __init__(self, event_type: str, event_data: _EventDataT):
        self._event_manager = apps.get_app_config("django_event_observer").event_manager
        self.event_type = event_type
        self.event_data = event_data

    def __call__(self):
        self.notify()

    def notify(self):
        self._event_manager.notify(self)

    def __str__(self):
        return f"{self.event_type}: {self.event_data}"

Accessing EventManager

To subscribe or unsubscribe an observer from specific event types, you need to access the initialized EventManager. It is recommended to do this using the Django applications registry:

from django.apps import apps

event_manager = apps.get_app_config("django_event_observer").event_manager

Subscribing to Events

To subscribe an observer to a specific event type:

from my_module.observers import MyObserver
from django.apps import apps

# Get the EventManager instance
event_manager = apps.get_app_config("django_event_observer").event_manager

# Create an observer instance
observer = MyObserver()

# Subscribe the observer to an event type
event_manager.subscribe("my_event_type", observer)

Unsubscribing from Events

To unsubscribe an observer from a specific event type:

# Unsubscribe the observer from the event type
event_manager.unsubscribe("my_event_type", observer)

Sending Events

To send an event and notify all subscribed observers, create an event instance and call the notify method:

from my_module.events import MyEvent

# Create an event instance
event = MyEvent(event_type="my_event_type", event_data={"key": "value"})

# Notify observers
event.notify()

Or you can call the event instance as a function thanks to the __call__ method:

# Notify observers by calling the event
event()

You can also use the EventManager directly to notify:

# Notify observers via EventManager
event_manager.notify(event)

Full Usage Example

# observers.py

from django_event_observer.observers.abstract.base import BaseAbstractObserver
from django_event_observer.events.base import BaseEvent

class MyObserver(BaseAbstractObserver):
    def update(self, event: BaseEvent) -> None:
        print(f"Observer received event: {event}")

# events.py

from django_event_observer.events.base import BaseEvent

class UserRegisteredEvent(BaseEvent[dict]):
    def __init__(self, user_data: dict):
        super().__init__(event_type="user_registered", event_data=user_data)

    def __str__(self):
        return f"UserRegisteredEvent: {self.event_data}"

# main.py

from django.apps import apps
from my_module.observers import MyObserver
from my_module.events import UserRegisteredEvent

# Get the EventManager instance
event_manager = apps.get_app_config("django_event_observer").event_manager

# Create an observer instance
observer = MyObserver()

# Subscribe the observer to the "user_registered" event
event_manager.subscribe("user_registered", observer)

# Create a user registration event
user_data = {"username": "john_doe", "email": "john@example.com"}
event = UserRegisteredEvent(user_data)

# Notify observers
event.notify()

# Or call the event as a function
event()

# Unsubscribe the observer when no longer needed
event_manager.unsubscribe("user_registered", observer)

Internal Structure of EventManager

The standard EventManager looks like this:

# django_event_observer/event_manager.py

from collections import defaultdict
import typing
from .observers.abstract.base import BaseAbstractObserver
from .events.base import BaseEvent

_ObserversT = dict[str, list[BaseAbstractObserver]]

class EventManager:
    _subscriptions: typing.ClassVar[_ObserversT] = defaultdict(list)

    def subscribe(self, event_type: str, observer: BaseAbstractObserver) -> None:
        self._subscriptions[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer: BaseAbstractObserver) -> None:
        self._subscriptions[event_type].remove(observer)

    def notify(self, event: BaseEvent) -> None:
        for observer in self._subscriptions.get(event.event_type, []):
            observer.update(event)

Additional Information

	•	Base Event Class: All events should inherit from django_event_observer.events.base.BaseEvent.
	•	EventManager Methods:
	•	subscribe(event_type: str, observer: BaseAbstractObserver): Subscribes an observer to an event type.
	•	unsubscribe(event_type: str, observer: BaseAbstractObserver): Unsubscribes an observer from an event type.
	•	notify(event: BaseEvent): Notifies all observers subscribed to event.event_type.
