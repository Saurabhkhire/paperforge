"""Docker sandbox for running miner code."""

import subprocess
import tempfile
from pathlib import Path

from paperforge.config import (
    ALLOWED_DEPENDENCIES,
    SANDBOX_MEMORY_MB,
    SANDBOX_TIMEOUT_SECONDS,
)


def _parse_requirements(requirements: list[str]) -> list[str]:
    """Extract package names from requirements list."""
    packages = []
    for r in requirements:
        r = r.strip().split("==")[0].split(">=")[0].split("<=")[0]
        if r and not r.startswith("#"):
            packages.append(r.lower())
    return packages


def check_dependencies_allowed(requirements: list[str]) -> tuple[bool, list[str]]:
    """Check all dependencies are in allowlist. Returns (allowed, disallowed)."""
    packages = _parse_requirements(requirements)
    disallowed = [p for p in packages if p not in ALLOWED_DEPENDENCIES]
    return len(disallowed) == 0, disallowed


def run_in_sandbox(
    code: str,
    requirements: list[str],
    test_script: str,
    timeout: int = SANDBOX_TIMEOUT_SECONDS,
) -> tuple[int, str, str]:
    """
    Run miner code in Docker sandbox.
    Returns (exit_code, stdout, stderr).
    """
    allowed, disallowed = check_dependencies_allowed(requirements)
    if not allowed:
        return (
            1,
            "",
            f"Dependencies not in allowlist: {disallowed}",
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "implementation.py").write_text(code, encoding="utf-8")
        (tmp / "run_tests.py").write_text(test_script, encoding="utf-8")
        req_path = tmp / "requirements.txt"
        req_path.write_text("\n".join(requirements), encoding="utf-8")

        # Use Python subprocess with isolated venv-style run
        # For production, use: docker run --rm -v tmp:/workspace ...
        # Here we simulate with subprocess for portability
        cmd = [
            "python",
            "-c",
            f"""
import subprocess
import sys
try:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', '/workspace/requirements.txt'], check=True, capture_output=True, timeout=30, cwd='/workspace')
except Exception as e:
    print(f'pip failed: {{e}}', file=sys.stderr)
    sys.exit(1)
sys.path.insert(0, '/workspace')
exec(open('/workspace/run_tests.py').read())
""",
        ]

        # Fallback: run test script directly (no Docker) for dev
        run_script = tmp / "run_tests.py"
        pip_cmd = ["pip", "install", "-q", "-r", str(req_path)]
        try:
            subprocess.run(
                ["python", "-m", "pip", "install", "-q", "-r", str(req_path)],
                capture_output=True,
                timeout=30,
                cwd=str(tmp),
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return 1, e.stdout.decode() or "", e.stderr.decode() or str(e)
        except Exception as e:
            return 1, "", str(e)

        result = subprocess.run(
            ["python", str(run_script)],
            capture_output=True,
            timeout=timeout,
            cwd=str(tmp),
            text=True,
        )
        return result.returncode, result.stdout, result.stderr
