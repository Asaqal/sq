"""Subprocess Exceptions."""

from enum import IntEnum


class SubprocessExitCode(IntEnum):
    """Exit codes returned by the subprocess.

    Attributes
    ----------
    SUCCESS : int
        The subprocess completed successfully.
    PATH_WRITE_ERROR : int
        An error occurred while reading the input from a ``.in`` path.
    DESERIALIZATION_ERROR : int
        An error occurred while deserializing the payload.
    TASK_EXECUTION_ERROR : int
        An error occurred while executing the task.
    SERIALIZATION_ERROR : int
        An error occurred while serializing the result.
    PATH_WRITE_ERROR : int
        An error occurred while writing the result to a ``.tmp`` path.
    """

    SUCCESS = 0
    PATH_READ_ERROR = 2
    DESERIALIZATION_ERROR = 3
    TASK_EXECUTION_ERROR = 4
    SERIALIZATION_ERROR = 5
    PATH_WRITE_ERROR = 6


class SubprocessError(Exception):
    """Base class for exceptions raised by the subprocess.

    Attributes
    ----------
    exit_code : SubprocessExitCode
        The exit code the subprocess returns when this exception is raised.
    """

    exit_code: SubprocessExitCode


class PathReadError(SubprocessError):
    """Raised when an error occurs while reading the input from a ``.in`` path."""

    exit_code = SubprocessExitCode.PATH_READ_ERROR


class DeserializationError(SubprocessError):
    """Raised when an error occurs while deserializing the payload."""

    exit_code = SubprocessExitCode.DESERIALIZATION_ERROR


class TaskExecutionError(SubprocessError):
    """Raised when an error occurs while executing the task."""

    exit_code = SubprocessExitCode.TASK_EXECUTION_ERROR


class SerializationError(SubprocessError):
    """Raised when an error occurs while serializing the result."""

    exit_code = SubprocessExitCode.SERIALIZATION_ERROR


class PathWriteError(SubprocessError):
    """Raised when an error occurs while writing the result to a ``.tmp`` path."""

    exit_code = SubprocessExitCode.PATH_WRITE_ERROR


"""
maybe collapse some of these exit codes if the logic doesn't change
or maybe keep them just so i have the scaffolding in case i ever want to do
something different per failure
like during retry policies?

could add a retry policy bool to each exception class
simplify the logic on the other side
"""
