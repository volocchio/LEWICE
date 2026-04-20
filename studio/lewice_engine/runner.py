"""
LEWICE Runner
Wraps the LEWICE executable for single and batch runs.
"""
import subprocess
import os
import shutil
import time


# Path to LEWICE executable relative to repo root
LEWICE_EXE = os.path.join(os.path.dirname(__file__), "..", "..", "lewice.exe")


def run_lewice(inp_file, xyd_file, work_dir=None, timeout=300):
    """Run a single LEWICE case.

    Args:
        inp_file: Path to .inp input file
        xyd_file: Path to .xyd geometry file
        work_dir: Working directory for the run (will be created if needed)
        timeout: Max seconds to wait for completion

    Returns:
        dict with status, output_dir, elapsed_time, stdout, stderr
    """
    exe = os.path.abspath(LEWICE_EXE)
    if not os.path.isfile(exe):
        return {"status": "error", "message": f"LEWICE executable not found: {exe}"}

    inp_file = os.path.abspath(inp_file)
    xyd_file = os.path.abspath(xyd_file)

    if work_dir is None:
        work_dir = os.path.join(os.path.dirname(inp_file), "run_output")
    os.makedirs(work_dir, exist_ok=True)

    # LEWICE reads input interactively: first the .inp path, then the .xyd path
    input_text = f"{inp_file}\n{xyd_file}\nY\n"

    # LEWICE is a Windows executable. On Linux hosts (e.g., VPS containers),
    # run it through Wine; on Windows, run it directly.
    if os.name == "nt":
        command = [exe]
    else:
        wine_cmd = (
            shutil.which("wine")
            or shutil.which("wine64")
            or ("/usr/lib/wine/wine64" if os.path.exists("/usr/lib/wine/wine64") else None)
            or "wine64"
        )
        command = [wine_cmd, exe]

    start = time.time()
    try:
        result = subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            text=True,
            cwd=work_dir,
            timeout=timeout,
        )
        elapsed = time.time() - start

        # Move output .dat files to work_dir (LEWICE writes to cwd)
        return {
            "status": "success" if result.returncode == 0 else "error",
            "return_code": result.returncode,
            "output_dir": work_dir,
            "elapsed_seconds": round(elapsed, 2),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": f"LEWICE exceeded {timeout}s timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def run_batch(cases, base_output_dir="batch_output"):
    """Run multiple LEWICE cases sequentially.

    Args:
        cases: list of dicts, each with keys: inp_file, xyd_file, case_name
        base_output_dir: parent directory for all case outputs

    Returns:
        list of result dicts
    """
    os.makedirs(base_output_dir, exist_ok=True)
    results = []
    total = len(cases)

    for i, case in enumerate(cases):
        case_name = case.get("case_name", f"case_{i+1:03d}")
        work_dir = os.path.join(base_output_dir, case_name)
        print(f"[{i+1}/{total}] Running {case_name}...")

        result = run_lewice(
            inp_file=case["inp_file"],
            xyd_file=case["xyd_file"],
            work_dir=work_dir,
        )
        result["case_name"] = case_name
        result["case_index"] = i + 1
        results.append(result)

        status = result["status"]
        elapsed = result.get("elapsed_seconds", "?")
        print(f"         -> {status} ({elapsed}s)")

    success = sum(1 for r in results if r["status"] == "success")
    print(f"\nBatch complete: {success}/{total} succeeded")
    return results


if __name__ == "__main__":
    print(f"LEWICE exe path: {os.path.abspath(LEWICE_EXE)}")
    print(f"Exists: {os.path.isfile(os.path.abspath(LEWICE_EXE))}")
