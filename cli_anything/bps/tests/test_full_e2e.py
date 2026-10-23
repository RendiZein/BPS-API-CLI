"""
Subprocess End-to-End Tests for BPS CLI Harness.
Tests live CLI execution, stream isolation, and multi-step agent journeys.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _resolve_cli(name: str = "bps") -> list[str]:
    """Resolve CLI executable: checks PATH, otherwise falls back to python -m module."""
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = "cli_anything.bps.bps_cli"
    return [sys.executable, "-m", module]


def _run_cli(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cli_base = _resolve_cli("bps")
    cmd = cli_base + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        raise AssertionError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result


def test_e2e_help_subprocess():
    """Verify bps --help executes cleanly and outputs usage."""
    result = _run_cli(["--help"])
    assert "Usage: bps" in result.stdout
    assert "status" in result.stdout
    assert "audit" in result.stdout


def test_e2e_status_json():
    """Verify bps status --json outputs parseable JSON to stdout."""
    result = _run_cli(["status", "--json"])
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert "status" in data
    assert "api_version" in data


def test_e2e_session_workflow():
    """Verify session init -> status -> undo workflow in subprocess."""
    # 1. Set domain
    res1 = _run_cli(["session", "set-domain", "3300", "--json"])
    data1 = json.loads(res1.stdout)
    assert data1["ok"] is True
    assert data1["domain"] == "3300"

    # 2. Status
    res2 = _run_cli(["session", "status", "--json"])
    data2 = json.loads(res2.stdout)
    assert data2["domain"] == "3300"

    # 3. Undo
    res3 = _run_cli(["session", "undo", "--json"])
    data3 = json.loads(res3.stdout)
    assert data3["ok"] is True

    # 4. Reset
    res4 = _run_cli(["session", "reset", "--json"])
    data4 = json.loads(res4.stdout)
    assert data4["ok"] is True
