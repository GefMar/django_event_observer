__all__ = ("ModelSignalEventEnum",)
from enum import StrEnum


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
