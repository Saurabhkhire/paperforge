"""Execution harness: runs miner code and produces scores."""

import json
from pathlib import Path

from .sandbox import run_in_sandbox
from .scoring import ValidationResult, compute_score

from paperforge.config import SANDBOX_TIMEOUT_SECONDS
from paperforge.miner.submission import MinerSubmission
from paperforge.task.schema import TaskSpec


def _build_test_script(task: TaskSpec) -> str:
    """Build the test script that runs in sandbox (local or Docker)."""
    # Pass sample_input as-is; if it's JSON string, implementation can parse it
    sample_input_repr = repr(task.sample_input)
    return f'''
import sys
import json

# Import miner implementation
from implementation import *

# Sample input (may be JSON string or raw)
sample_input_raw = {sample_input_repr}
try:
    sample_input = json.loads(sample_input_raw) if isinstance(sample_input_raw, str) and sample_input_raw.strip().startswith(("{{", "[")) else sample_input_raw
except Exception:
    sample_input = sample_input_raw

# Execution test
try:
    result = main(sample_input)
    exec_ok = True
except Exception as e:
    result = None
    exec_ok = False
    print(json.dumps({{"execution_pass": False, "error": str(e)}}), file=sys.stderr)
    sys.exit(1)

# Output for harness (normalize dict to JSON string for comparison)
out_str = json.dumps(result, sort_keys=True) if isinstance(result, dict) else str(result)
print(json.dumps({{"execution_pass": exec_ok, "sample_output": out_str}}))
'''


def run_validation(
    submission: MinerSubmission,
    task: TaskSpec,
    task_dir: Path | None = None,
) -> ValidationResult:
    """
    Run full validation: execution, hidden tests, performance.
    Returns ValidationResult with scores.
    """
    test_script = _build_test_script(task)

    exit_code, stdout, stderr = run_in_sandbox(
        code=submission.code,
        requirements=submission.requirements,
        test_script=test_script,
        timeout=SANDBOX_TIMEOUT_SECONDS,
    )

    execution_pass = exit_code == 0

    # Parse stdout for sample output match (normalize JSON for comparison)
    correctness_frac = 0.0
    if execution_pass and stdout.strip():
        try:
            data = json.loads(stdout.strip().split("\n")[-1])
            sample_out = data.get("sample_output", "")
            expected = task.sample_output.strip()
            try:
                expected_obj = json.loads(expected)
                sample_obj = json.loads(sample_out) if isinstance(sample_out, str) else sample_out
                match = (
                    json.dumps(expected_obj, sort_keys=True) == json.dumps(sample_obj, sort_keys=True)
                    if isinstance(sample_obj, dict)
                    else (sample_out == expected)
                )
            except Exception:
                match = (sample_out == expected)
            # Sample test counts as one correctness check; with 5 hidden tests would be 1/5 each
            correctness_frac = 1.0 if match else 0.0
        except Exception:
            correctness_frac = 0.0

    # If we have hidden tests (future: run them in sandbox), could blend with correctness_frac
    if task_dir and (Path(task_dir) / "hidden_tests.py").exists() and correctness_frac == 0.0 and execution_pass:
        correctness_frac = 0.5  # placeholder when no sample match but hidden tests exist

    # Performance: placeholder (would run benchmark script)
    performance_frac = 0.25 if execution_pass else 0.0

    result = compute_score(
        execution_pass=execution_pass,
        correctness_frac=correctness_frac,
        performance_frac=performance_frac,
    )
    result.details["stdout"] = stdout
    result.details["stderr"] = stderr
    result.details["exit_code"] = exit_code
    return result
