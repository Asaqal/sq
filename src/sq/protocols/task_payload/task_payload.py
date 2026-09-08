"""TODO."""

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable


class TaskPayload(Protocol):
    """Interface for payloads used to execute a task.

    Implementations provide a callable along with the positional and keyword
    arguments required to invoke it.

    Attributes
    ----------
    func : Callable[..., Any]
        Callable representing the task to execute.
    args : tuple[Any, ...]
        Positional arguments to pass to `func`.
    kwargs : dict[str, Any]
        Keyword arguments to pass to `func`.
    """

    @property
    def func(self) -> Callable[..., Any]:
        """Return the callable representing the task.

        Returns
        -------
        Callable[..., Any]
            Task callable to execute.
        """
        ...

    @property
    def args(self) -> tuple[Any, ...]:
        """Return the positional arguments for the task.

        Returns
        -------
        tuple[Any, ...]
            Positional arguments to pass to `func`.
        """
        ...

    @property
    def kwargs(self) -> dict[str, Any]:
        """Return the keyword arguments for the task.

        Returns
        -------
        dict[str, Any]
            Keyword arguments to pass to `func`.
        """
        ...


"""
TODO
update the docstrings/ai garbage
"""
