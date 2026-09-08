"""Subprocess."""

import json
import sys
from pathlib import Path

from sq.exe.exceptions import (
    DeserializationError,
    PathReadError,
    PathWriteError,
    SerializationError,
    SubprocessError,
    TaskExecutionError,
)
from sq.protocols import TaskPayload
from sq.utils import deserialize, serialize


def main() -> int:
    """Execute a single task in its own subprocess.

    Read the ``task_id`` from ``sys.argv``, read the ``.in`` path, deserialize the payload,
    execute the task, serialize the result, and write it to a ``.tmp`` path.

    Returns
    -------
    int
        Exit code ``0``: The subprocess completed successfully.

    Raises
    ------
    PathReadError
        Exit code ``2``: An error occurred while reading the input from a ``.in`` path.
    DeserializationError
        Exit code ``3``: An error occurred while deserializing the payload.
    TaskExecutionError
        Exit code ``4``: An error occurred while executing the task.
    SerializationError
        Exit code ``5``: An error occurred while serializing the result.
    PathWriteError
        Exit code ``6``: An error occurred while writing the result to a ``.tmp`` path.
    """
    task_id = int(sys.argv[1])

    envelope_path = Path(f".local/{task_id}/{task_id}.in")  # ! DIFFERENT VARIABLE NAME?
    try:
        envelope = json.loads(envelope_path.read_text())
        serialized_task_payload = envelope["serialized_task_payload"]
    except Exception as e:
        err_msg = (
            f"An error occurred while reading task-{task_id}'s input from {envelope_path}: {e}"
        )
        raise PathReadError(err_msg) from e

    try:
        task_payload = deserialize(serialized_task_payload, TaskPayload)
    except Exception as e:
        err_msg = f"An error occurred while deserializing task-{task_id}'s payload: {e}"
        raise DeserializationError(err_msg) from e

    try:
        task_result = task_payload.func(*task_payload.args, **task_payload.kwargs)
    except Exception as e:
        err_msg = f"An error occurred while executing task-{task_id}: {e}"
        raise TaskExecutionError(err_msg) from e

    try:
        serialized_task_result = serialize(task_result)
    except Exception as e:
        err_msg = f"An error occurred while serializing task-{task_id}'s result: {e}"
        raise SerializationError(err_msg) from e

    result_path = Path(f".local/{task_id}/{task_id}.tmp")  # ! figure out actual directory system
    try:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(serialized_task_result)
    except Exception as e:
        errmsg = f"An error occurred while writing task-{task_id}'s result to {result_path}: {e}"
        raise PathWriteError(errmsg) from e

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SubprocessError as e:
        sys.exit(e.exit_code)

"""
TODO
it will also receive all of the extra heuristics
like runtime, memory usage, etc. (maybe make an optional verbose flag?)

like if it's a task failure, then maybe don't retry
but if it's a system failure, then maybe retry

make a util function for writing to path
can be reused in worker code for .out and .err files

instead of writing to .local, figure out the actual directory

change starting input variable names
"""
