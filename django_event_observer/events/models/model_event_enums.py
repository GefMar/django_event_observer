__all__ = ("ModelSignalEventEnum",)

# flake8: noqa

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore
        pass


class ModelSignalEventEnum(StrEnum):
    PRE_INIT = "pre_init"
    POST_INIT = "post_init"
    PRE_SAVE = "pre_save"
    POST_SAVE = "post_save"
    PRE_DELETE = "pre_delete"
    POST_DELETE = "pre_delete"
    M2M_CHANGED = "m2m_changed"
    PRE_MIGRATE = "pre_migrate"
    POST_MIGRATE = "post_migrate"
