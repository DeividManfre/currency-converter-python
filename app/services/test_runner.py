import subprocess
import os
import sys

LOG_DIR = "/app/tests/test_logs"

class TestRunner:
    @staticmethod
    def run_tests():
        os.makedirs(LOG_DIR, exist_ok=True)

        if "/app" not in sys.path:
            sys.path.insert(0, "/app")

        env = os.environ.copy()
        env["PYTHONPATH"] = "/app"

        pytest_cmd = [
            "pytest",
            "-vv",
            "--maxfail=1",
            "--disable-warnings",
            "--rootdir=/app",
        ]

        result = subprocess.run(
            pytest_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/app",
            env=env
        )

        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
