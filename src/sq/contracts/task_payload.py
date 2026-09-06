"""Contract for a payload of a function call to serialize, transmit, and execute in a subprocess."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class TaskPayload:
    """Payload of a function call to serialize, transmit, and execute in a subprocess.

    Attributes
    ----------
    func : Callable[..., Any]
        The task to execute.
    args : tuple[Any, ...]
        Positional arguments to pass to `func`.
    kwargs : dict[str, Any]
        Keyword arguments to pass to `func`.
    """

    func: Callable[..., Any]
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
