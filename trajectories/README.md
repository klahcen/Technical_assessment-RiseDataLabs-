# Saved Harbor job outputs

| Directory | Agent / model | Outcome |
|-----------|---------------|---------|
| `oracle-reward-1/` | oracle | **reward = 1.0** — gold patch applied; task is solvable |
| `terminus-2-deepseek-chat-reward-0/` | terminus-2 / `deepseek/deepseek-chat` | **Completed trial**, reward = 0.0 (~7m, ~$0.02) |

## Primary artifacts for review

1. **Oracle** — proves the environment + verifier + gold solution work end-to-end.
2. **DeepSeek agent** — real terminus-2 run with full `trajectory.json`; verifier correctly scored 0 because FAIL_TO_PASS tests still failed (bug not fixed by the agent).
