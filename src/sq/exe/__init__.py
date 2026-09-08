"""Execute a single task in its own subprocess."""

from sq.exe.exe import main

__all__ = ["main"]

"""
TODO
import more/expose exceptions maybe for worker so it can handle them better?
either SubprocessError or SubprocessExitCode
"""
