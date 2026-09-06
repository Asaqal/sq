"""Exceptions."""

from enum import IntEnum


class SubprocessExitCode(IntEnum):
    """Exit codes returned by the subprocess executor.

    Attributes
    ----------
    SUCCESS : int
        The subprocess completed successfully.
    DESERIALIZATION_ERROR : int
        An error occurred during task-payload deserialization.
    TASK_EXECUTION_ERROR : int
        An error occurred during task execution.
    SERIALIZATION_ERROR : int
        An error occurred during task-result serialization.
    PATH_WRITE_ERROR : int
        An error occurred while writing the task-result to a .tmp path.
    """

    SUCCESS = 0
    DESERIALIZATION_ERROR = 2
    TASK_EXECUTION_ERROR = 3
    SERIALIZATION_ERROR = 4
    PATH_WRITE_ERROR = 5


class SubprocessError(Exception):
    """Base class for exceptions raised by the subprocess executor.

    Attributes
    ----------
    exit_code : SubprocessExitCode
        The exit code the subprocess returns when this exception is raised.
    """

    exit_code: SubprocessExitCode


class DeserializationError(SubprocessError):
    """Raised when an error occurs during task-payload deserialization."""

    exit_code = SubprocessExitCode.DESERIALIZATION_ERROR


class TaskExecutionError(SubprocessError):
    """Raised when an error occurs during task execution."""

    exit_code = SubprocessExitCode.TASK_EXECUTION_ERROR


class SerializationError(SubprocessError):
    """Raised when an error occurs during task-result serialization."""

    exit_code = SubprocessExitCode.SERIALIZATION_ERROR


class PathWriteError(SubprocessError):
    """Raised when an error occurs while writing the task-result to a ``.tmp`` path."""

    exit_code = SubprocessExitCode.PATH_WRITE_ERROR


"""
maybe collapse some of these exit codes if the logic doesn't change
or maybe keep them just so i have the scaffolding in case i ever want to do
something different per failure
like during retry policies?
"""
