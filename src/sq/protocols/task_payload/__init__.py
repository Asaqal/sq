"""TODO."""

from sq.protocols.task_payload.direct_task_payload import DirectTaskPayload
from sq.protocols.task_payload.task_payload import TaskPayload

try:
    from sq.protocols.task_payload.coffea_task_payload import CoffeaTaskPayload
except ImportError as e:
    err_msg = "CoffeaTaskPayload requires `uv pip install sq[coffea]`."
    raise ImportError(err_msg) from e


__all__ = ["CoffeaTaskPayload", "DirectTaskPayload", "TaskPayload"]
