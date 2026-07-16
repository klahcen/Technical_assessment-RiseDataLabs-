# Design: swebench-pylint-unrecognized-option

## Source / inspiration

Adapted from **SWE-bench Lite** (paper: https://arxiv.org/abs/2310.06770, https://www.swebench.com).

| Field | Value |
|-------|-------|
| **SWE-bench Lite `instance_id`** | `pylint-dev__pylint-6506` |
| **Repo** | `pylint-dev/pylint` |
| **Base commit** | `0a4204fd7555cfedd43f43017c94d24ef48244a5` |
| **Version (SWE-bench)** | `2.14` |

Selected because the gold patch is tiny (one file, ~3 changed lines), `FAIL_TO_PASS` has exactly two tests, `PASS_TO_PASS` is only six tests in the same file, and pylint is lightweight to install compared to Django / SciPy-stack repos.

Packaged as a single **Harbor** task (https://www.harborframework.com) rather than running the full SWE-bench evaluation harness.

## What the bug / tests cover

Unrecognized CLI options (e.g. `pylint -Q` or `--unknown-option=yes`) used to:

1. Emit an `unrecognized-option` message, then
2. Raise internal `_UnrecognizedOptionError`, which dumped a traceback.

The expected UX is to exit via the argument parser (`ArgumentParser.error`) with a usage message and no traceback.

- **FAIL_TO_PASS**: `test_unknown_option_name`, `test_unknown_short_option_name` — after `test_patch`, these expect `SystemExit` and stderr containing `usage: pylint` / `Unrecognized option`.
- **PASS_TO_PASS**: six neighboring config tests (toml env var, unknown message id / confidence / yes-no / py-version, short verbose) that must stay green.

## What we changed vs. the official SWE-bench harness

| Aspect | Official SWE-bench | This Harbor task |
|--------|--------------------|------------------|
| Environment | Multi-layer conda/Docker images (`SPECS_PYLINT`, Python 3.9) | Single `python:3.9-bookworm` Dockerfile cloning the repo at `base_commit` |
| Install | `packages: requirements.txt` + `pip install -e .` (plus harness helpers) | Explicit pip pins aligned with `requirements_test_min.txt` / `setup.cfg`, then `pip install -e .` |
| Spelling extra | Often includes `pyenchant` / `[spelling]` | **Omitted** — not needed for these tests; avoids `libenchant` system deps |
| `pytest-benchmark` | Present in `requirements_test_min.txt` | **Omitted** — conflicts (`py.io` / shadowed `py`) and unused here |
| Evaluation | Harness applies prediction patch + `test_patch`, runs listed tests | Harbor oracle applies `solution/fix.patch`; verifier applies `tests/test_patch.patch` then runs FAIL_TO_PASS + PASS_TO_PASS via `tests/test_outputs.py` |
| Scope | Full SWE-bench instance image + harness logging | One self-contained Harbor task directory |

## Validation results

| Run | Result |
|-----|--------|
| Manual Docker (no fix) | FAIL_TO_PASS fail; PASS_TO_PASS pass |
| Manual Docker (with gold fix) | All relevant tests pass |
| `harbor run -a oracle` | **reward = 1.0** |
| `harbor run -a terminus-2 -m deepseek/deepseek-chat` | Completed trial, **reward = 0.0** (agent did not apply the fix) |

Artifacts: `trajectories/oracle-reward-1/` and `trajectories/terminus-2-deepseek-chat-reward-0/`.

## Known limitations

1. **Network at build time**: The Dockerfile `git clone`s GitHub; image build needs outbound network.
2. **Not a full SWE-bench harness clone**: No conda, no `environment_setup_commit` dance, no nano_cpus limits — only what these tests need.
3. **Editable install**: Agents edit `/app` source; the image uses `pip install -e .` so changes are picked up without reinstall.
4. **Test patch is verifier-owned**: Agents should not need to modify tests; the verifier applies `test_patch.patch` after the agent finishes.
5. **Agent reward 0 is expected / informative**: The task is non-trivial for a small model; oracle=1 shows solvability, agent=0 shows the verifier discriminates correctly.
