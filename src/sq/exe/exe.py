"""Subprocess Executor."""

import sys
from pathlib import Path

from sq.contracts.task_payload import TaskPayload
from sq.exe.exceptions import (
    PathWriteError,
    SerializationError,
    SubprocessError,
    TaskExecutionError,
)
from sq.utils import deserialize, serialize


def main() -> int:
    """Execute a single task in its own subprocess.

    Read arguments from `sys.argv`, deserialize the task-payload, execute the task,
    serialize the result, and write it to a .tmp path.

    Returns
    -------
    int
        Exit code ``0``: The subprocess completed successfully.

    Raises
    ------
    SerializationError
        Exit code ``2``: An error occurred during task-payload deserialization.
    TaskExecutionError
        Exit code ``3``: An error occurred during task execution.
    SerializationError
        Exit code ``2``: An error occurred during task-result serialization.
    PathWriteError
        Exit code ``4``: An error occurred while writing the task-result to a .tmp path.
    """
    task_id = int(sys.argv[1])
    serialized_task_payload = sys.argv[2]

    try:
        task_payload = deserialize(serialized_task_payload, TaskPayload)
    except Exception as e:
        err_msg = f"An error occurred during task-{task_id}'s payload deserialization: {e}"
        raise SerializationError(err_msg) from e

    try:
        task_result = task_payload.func(*task_payload.args, **task_payload.kwargs)
    except Exception as e:
        err_msg = f"An error occurred during task-{task_id}'s execution: {e}"
        raise TaskExecutionError(err_msg) from e

    try:
        serialized_task_result = serialize(task_result)
    except Exception as e:
        err_msg = f"An error occurred during task-{task_id}'s result serialization: {e}"
        raise SerializationError(err_msg) from e

    path = Path(f".local/{task_id}/{task_id}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(serialized_task_result)
    except Exception as e:
        errmsg = f"An error occurred while writing task-{task_id}'s result to {path}: {e}"
        raise PathWriteError(errmsg) from e

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SubprocessError as e:
        sys.exit(e.exit_code)

"""
it will also receive all of the extra heuristics
like runtime, memory usage, etc. (maybe make an optional verbose flag?)

like if it's a task failure, then maybe don't retry
but if it's a system failure, then maybe retry

make a util function for writing to path
can be reused in worker code for .out and .err files

instead of writing to .local, figure out the actual directory
"""
