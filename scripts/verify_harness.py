"""
Automated Linter and Compliance Validator for BPS Agent-Native Harness.
Validates directory structure, JSON configurations, documentation, and test suite.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def check_file(path_str: str, desc: str) -> bool:
    p = Path(path_str)
    if p.exists():
        print(f"  [OK] {desc}: {path_str}")
        return True
    else:
        print(f"  [FAIL] {desc} MISSING: {path_str}")
        return False


def check_json(path_str: str) -> bool:
    p = Path(path_str)
    try:
        with open(p, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"  [OK] Valid JSON: {path_str}")
        return True
    except Exception as e:
        print(f"  [FAIL] Invalid JSON in {path_str}: {e}")
        return False


def main():
    print("=" * 60)
    print("BPS Agent-Native Harness Compliance Verification")
    print("=" * 60)

    errors = 0

    print("\n[1] Checking Required Files & Specifications:")
    required_files = [
        ("plugin.json", "Antigravity Plugin Manifest"),
        ("setup.py", "PEP 420 Packaging Setup"),
        ("BPS.md", "Domain Architecture Specification"),
        ("coverage.matrix.json", "Traceability & Coverage Contract"),
        ("skills/bps-api/SKILL.md", "Canonical Agent SKILL.md"),
        ("grand_plan_bps_api_cli.md", "Grand Master Plan"),
    ]
    for rel_path, desc in required_files:
        if not check_file(rel_path, desc):
            errors += 1

    print("\n[2] Validating JSON Manifests:")
    json_files = ["plugin.json", "coverage.matrix.json"]
    for jf in json_files:
        if not check_json(jf):
            errors += 1

    print("\n[3] Validating SKILL.md Frontmatter:")
    skill_path = Path("skills/bps-api/SKILL.md")
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        if text.startswith("---") and "name: bps-api-analyst" in text:
            print("  [OK] SKILL.md YAML frontmatter is valid")
        else:
            print("  [FAIL] SKILL.md frontmatter missing or invalid")
            errors += 1
    else:
        errors += 1

    print("\n[4] Running Pytest Test Suite:")
    res = subprocess.run([sys.executable, "-m", "pytest", "cli_anything/bps/tests", "-q"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [OK] Test Suite: 100% Passing ({res.stdout.strip()})")
    else:
        print(f"  [FAIL] Test Suite Failed:\n{res.stdout}\n{res.stderr}")
        errors += 1

    print("\n" + "=" * 60)
    if errors == 0:
        print("[SUCCESS] All validation checks PASSED! Harness is production-ready.")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"[FAIL] Found {errors} error(s). Please fix before deployment.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
