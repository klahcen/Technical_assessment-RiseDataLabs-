"""Verifier for pylint-dev__pylint-6506.

Runs the SWE-bench Lite FAIL_TO_PASS and PASS_TO_PASS tests against the
/app pylint checkout (after tests/test.sh has applied test_patch.patch).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_DIR = Path("/app")

FAIL_TO_PASS = [
    "tests/config/test_config.py::test_unknown_option_name",
    "tests/config/test_config.py::test_unknown_short_option_name",
]

PASS_TO_PASS = [
    "tests/config/test_config.py::test_can_read_toml_env_variable",
    "tests/config/test_config.py::test_unknown_message_id",
    "tests/config/test_config.py::test_unknown_confidence",
    "tests/config/test_config.py::test_unknown_yes_no",
    "tests/config/test_config.py::test_unknown_py_version",
    "tests/config/test_config.py::test_short_verbose",
]


def _run_pytest(node_ids: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pytest", *node_ids, "-q", "--tb=short"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_fail_to_pass_tests_now_pass() -> None:
    """Tests that failed on the buggy base commit must pass after the fix."""
    result = _run_pytest(FAIL_TO_PASS)
    assert result.returncode == 0, (
        "FAIL_TO_PASS tests did not all pass.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_pass_to_pass_tests_still_pass() -> None:
    """Regression suite that already passed must remain green."""
    result = _run_pytest(PASS_TO_PASS)
    assert result.returncode == 0, (
        "PASS_TO_PASS tests failed (possible regression).\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
