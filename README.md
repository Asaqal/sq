sq (saqal hq (hep-queue))

Read the [docs](https://asaqal.github.io/sq/)

TODO:
input schema -> heavykey or some other alternative?

need workers to cache payload's and serve that to the subprocess first if it already exists

i still dont understand the whole heavy key thing and how the work submitted by the client
is being granulated and delivered to the subprocesses

imperative docstrings throughout
add mermaid/other diagarams per module to explain how it all interacts
can even do it for specific function doc strings, to ensure it's clear

sphinx is broken on contracts/task_payload.py's function signature
overall, a lot of duping with the way my __init__.py is setup