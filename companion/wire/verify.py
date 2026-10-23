"""Demonstrate weak-green, corrected-red, and repaired-green; exit 0 on success."""

from pathlib import Path
import os
import subprocess
import sys


def run_test(label, implementation, target, expect_defect=False):
    environment = dict(os.environ, WIRE_IMPLEMENTATION=implementation,
                       PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", target],
        cwd=Path(__file__).resolve().parent,
        env=environment, capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    print(f"\n{label}\n{output}", flush=True)
    if expect_defect:
        # A random import error or unrelated failure is not the intended lesson.
        expected = (result.returncode == 1
                    and "AssertionError: None != 'URGENT'" in output
                    and "Ran 1 test" in output
                    and "FAILED (failures=1)" in output)
    else:
        expected = result.returncode == 0
    if not expected:
        raise SystemExit(f"Unexpected outcome: {label}")


if __name__ == "__main__":
    run_test("1. Inadequate assertion: green on defective code",
             "defective", "tests.LegacyAssertion")
    run_test("2. Corrected assertion: expected red on defective code",
             "defective", "tests.AuditContract", expect_defect=True)
    run_test("3. Repaired implementation: all acceptance checks green",
             "wire", "tests")
    print("PASS: observed the intended defect and verified the repair.")
