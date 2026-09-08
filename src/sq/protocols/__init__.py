"""TODO."""

from sq.protocols.task_payload import DirectTaskPayload, TaskPayload

try:
    from sq.protocols.task_payload import CoffeaTaskPayload
except ImportError as e:
    err_msg = "CoffeaTaskPayload requires `uv pip install sq[coffea]`."
    raise ImportError(err_msg) from e


__all__ = ["CoffeaTaskPayload", "DirectTaskPayload", "TaskPayload"]
