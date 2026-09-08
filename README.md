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

maybe also add an environment path to task_payload protocol
but how do i know where the environments live on the worker?
it's not like you can use an environment from a file
-> add it to the input file, which contains a json of just two elements
``interpreter_path`` and ``serialized_task_payload``

if i have retry policies baked into the subprocess error codes
then if the worker follows those and tries them on their own
it needs to have a system to stop after X retries
or just have it send back a failure ack with a retry yes or no bool
instead of an ack it should be in the .err or .out file