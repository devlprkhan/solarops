"""Start FastAPI backend and Streamlit dashboard together for local development."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    backend = [
        sys.executable,
        "-m",
        "uvicorn",
        "solarops_api.main:app",
        "--app-dir",
        str(ROOT / "apps" / "api"),
        "--reload",
    ]
    frontend = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "apps" / "dashboard" / "app.py"),
    ]

    print("Starting FastAPI backend on http://127.0.0.1:8000")
    print("Starting Streamlit dashboard on http://localhost:8501")
    print("Press Ctrl+C to stop both.\n")

    backend_proc = subprocess.Popen(backend, cwd=ROOT)
    frontend_proc = subprocess.Popen(frontend, cwd=ROOT)
    processes = [backend_proc, frontend_proc]

    try:
        while True:
            for proc in processes:
                if proc.poll() is not None:
                    raise RuntimeError(f"A process exited unexpectedly with code {proc.returncode}.")
            time.sleep(0.5)
    except (KeyboardInterrupt, RuntimeError) as exc:
        print(f"\nStopping development processes: {exc}")
    finally:
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
        for proc in processes:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()