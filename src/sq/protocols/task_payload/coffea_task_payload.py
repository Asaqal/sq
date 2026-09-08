"""TODO."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any

from sq.utils import deserialize

try:
    from coffea.processor.executor import WorkItem
except ImportError as e:
    err_msg = "CoffeaTaskPayload requires `uv pip install sq[coffea]`."
    raise ImportError(err_msg) from e

if TYPE_CHECKING:
    from pathlib import Path

    from coffea.processor.executor import WorkItem


@dataclass
class CoffeaTaskPayload:
    """Payload for executing a serialized function with a Coffea work item.

    Parameters
    ----------
    _serialized_func_path : Path
        Path to the serialized task function.
    _work_item : WorkItem
        Coffea work item to pass to the task function.

    Attributes
    ----------
    func : Callable[[WorkItem], Any]
        The task to execute.
    args : tuple[WorkItem, ...]
        Positional arguments to pass to `func`.
    kwargs : dict[str, Any]
        Keyword arguments to pass to `func`.
    """

    _serialized_func_path: Path
    _work_item: WorkItem

    @property
    def func(self) -> Callable[[WorkItem], Any]:
        """Return the deserialized task function.

        Returns
        -------
        Callable[[WorkItem], Any]
            Task function deserialized from `_serialized_func_path`.
        """
        return deserialize(self._serialized_func_path.read_text(), Callable)

    @cached_property
    def args(self) -> tuple[WorkItem, ...]:
        """Return the positional arguments for the task function.

        Returns
        -------
        tuple[WorkItem, ...]
            Tuple containing the work item passed to the task function.
        """
        return (self._work_item,)

    @cached_property
    def kwargs(self) -> dict[str, Any]:
        """Return the keyword arguments for the task function.

        Returns
        -------
        dict[str, Any]
            Empty dictionary, as this payload does not provide keyword
            arguments.
        """
        return {}


"""
TODO
rename the parameters and update docstrings accordingly
these are garbage
"""
