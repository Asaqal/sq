sq documentation
================

.. mermaid::

   flowchart TD
      subgraph Client["Client (submitter)"]
         C1["HQExecutor / CoffeaHQExecutor"]
         C2["wait / gather"]
      end

      subgraph Server["Bun HTTP facade + Redis"]
         S1["fetch: atomic RPOP + mark running + tag worker_id"]
         S2["Heartbeat receiver<br/>(per-task running list + pending-ack completions)"]
         S3["Ack completions,<br/>drop from next heartbeat"]
         S4["Stuck-task detector<br/>(elapsed time per task)"]
         S5["Dead-worker sweep<br/>(triggered on heartbeat loss)"]
         S6["Dispatch verify-task<br/>for each orphaned task_id"]
      end

      subgraph WorkerA["Worker (normal operation)"]
         W1["Popen(exe.py, task_id)<br/>PR_SET_PDEATHSIG=SIGKILL"]
         W2["Subprocess writes<br/>task_id.pkl.tmp"]
         W3{"Exit code?"}
         W4["Deserialize .tmp"]
         W5{"Deserializes OK?"}
         W6["Rename .tmp → .pkl<br/>(certified success)"]
         W7["Rename .tmp → .tmp.bad<br/>capture stderr traceback"]
         W8["Report terminal status<br/>(pending ack in heartbeat)"]
      end

      subgraph WorkerB["Other live worker (recovery)"]
         V1["Picks up verify-task<br/>via normal fetch/claim"]
         V2["Deserialize target .pkl / .tmp.bad / .tmp"]
         V3{"File state?"}
         V4[".pkl valid → success"]
         V5[".tmp.bad → error, evidence kept"]
         V6[".tmp or missing → lost"]
         V7["Report outcome to server"]
      end

      FS[("Shared Filesystem<br/>HQ_RESULT_DIR")]

      C1 -->|submit tasks| S1
      S1 -->|claim| W1
      W1 --> W2
      W2 --> FS
      W2 --> W3
      W3 -->|non-zero| W7
      W3 -->|zero| W4
      W4 --> W5
      W5 -->|no| W7
      W5 -->|yes| W6
      W6 --> FS
      W6 --> W8
      W7 --> W8
      W8 -->|heartbeat tick| S2
      S2 --> S3
      S2 --> S4
      S4 -.flag stuck.-> C2

      W1 -.worker dies.-> S2
      S2 -.heartbeat lost.-> S5
      S5 --> S6
      S6 -->|dispatch as task| V1
      V1 --> V2
      V2 --> FS
      V2 --> V3
      V3 -->|pkl valid| V4
      V3 -->|tmp.bad| V5
      V3 -->|tmp / nothing| V6
      V4 --> V7
      V5 --> V7
      V6 --> V7
      V7 --> S1
      V6 -.requeue as new task if lost.-> S1

      S3 -->|status updates| C2
      C2 -->|gather via resultPath| FS


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/modules