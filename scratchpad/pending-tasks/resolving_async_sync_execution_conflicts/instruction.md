A common friction point in Prefect is mixing asynchronous tasks with synchronous flows, which frequently results in a `RuntimeError: This event loop is already running`.

You need to debug and fix a provided Prefect script where a synchronous `@flow` incorrectly attempts to call an asynchronous `@task`. 

**Constraints:**
- Do NOT change the asynchronous nature of the inner task (it must remain defined with `async def`).
- Refactor the code (either by updating the flow definition or the task invocation) so the event loop handles the async execution without throwing an error.
- The flow must execute successfully and return the expected computed string.