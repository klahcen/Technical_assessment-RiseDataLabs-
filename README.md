# swebench-pylint-unrecognized-option

Harbor task adapted from **SWE-bench Lite** instance `pylint-dev__pylint-6506`: fix pylint so unrecognized CLI options exit cleanly (usage + error) instead of raising `_UnrecognizedOptionError` with a traceback.

See [DESIGN.md](./DESIGN.md) for design notes, harness differences, and validation results.

## Results (captured)

| Agent | Model | Reward |
|-------|-------|--------|
| oracle | — | **1.0** |
| terminus-2 | deepseek/deepseek-chat | **0.0** (completed trial; bug not fixed) |

Saved under [`trajectories/`](./trajectories/).

## Prerequisites

- Docker
- Python 3.12+ with [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Harbor: `uv tool install harbor` or `pip install harbor`
- For real-agent runs: a LiteLLM-compatible API key (e.g. `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`) with credits

## Setup

From this repository root:

```bash
uv tool install harbor   # or: pip install harbor

# Optional: pre-build the environment image
docker build -t swebench-pylint-unrecognized-option \
  -f environment/Dockerfile .
```

## Run

Oracle (gold patch) — expect reward `1.0`:

```bash
harbor run -p . -a oracle
```

Real agent examples:

```bash
export DEEPSEEK_API_KEY=...
harbor run -p . -a terminus-2 -m deepseek/deepseek-chat

# or
export ANTHROPIC_API_KEY=...
harbor run -p . -a terminus-2 -m anthropic/claude-haiku-4-5
```

Inspect jobs:

```bash
harbor view jobs
```

## Assumptions & limitations

- **Network**: Docker build clones `https://github.com/pylint-dev/pylint.git` and installs packages from PyPI.
- **Python**: Image uses **Python 3.9** (matches SWE-bench `SPECS_PYLINT` for version 2.14).
- **Repo checkout**: Fixed at base commit `0a4204fd7555cfedd43f43017c94d24ef48244a5` under `/app`.
- **Verifier**: Applies `tests/test_patch.patch`, then requires both FAIL_TO_PASS and PASS_TO_PASS tests to pass (`tests/test_outputs.py`).
- **Optional deps dropped**: `pytest-benchmark` and `pyenchant`/spelling extras are not installed (unneeded for this instance; see DESIGN.md).

## Layout

```
.
├── instruction.md          # Agent-facing bug description
├── task.toml               # Metadata & timeouts
├── DESIGN.md
├── README.md
├── instance.json           # SWE-bench Lite metadata snapshot
├── environment/Dockerfile  # Clone + install pylint @ base_commit
├── solution/
│   ├── fix.patch           # Gold patch
│   └── solve.sh            # git apply fix.patch
├── tests/
│   ├── test_patch.patch    # SWE-bench test patch
│   ├── test.sh             # Apply test patch + run verifier
│   └── test_outputs.py     # Assert FAIL_TO_PASS & PASS_TO_PASS
└── trajectories/           # Oracle + DeepSeek agent job outputs
```

## Inspiration

- [SWE-bench](https://www.swebench.com) / [SWE-bench Lite](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Lite)
- [Harbor](https://www.harborframework.com)
