"""
LEWICE Runner
Wraps the NASA LEWICE 3.2 executable for single and batch runs.

LEWICE prompts for the namelist path, then the geometry path, then 'Y' to
continue past warnings. On Linux the shipped binary is the Windows
lewice.exe. Piping stdin/stdout into Wine breaks the Compaq/Intel Fortran
runtime ("forrtl: severe (38): error during write, unit -1, file CONOUT$"),
so the Wine path feeds LEWICE through files from a batch script instead.
"""
import os
import shutil
import subprocess
import time


# Path to the Windows LEWICE executable shipped at the repo root.
LEWICE_EXE = os.path.join(os.path.dirname(__file__), "..", "..", "lewice.exe")

_RESPONSE_LINES = 8  # extra "Y" answers so a warning prompt cannot stall the run


def _wine_path(path):
    """Map a POSIX path to the Wine Z: drive."""
    absolute = os.path.abspath(path)
    return "Z:" + absolute.replace("/", "\\")


def probe_lewice(exe_path=None):
    """Say whether a run can actually be launched, and how.

    A present lewice.exe is not enough on Linux: Wine has to be installed,
    because the Fortran console executable cannot be executed natively.
    """
    exe = os.path.abspath(exe_path or LEWICE_EXE)
    if os.name == "nt":
        if os.path.isfile(exe):
            return {
                "ok": True,
                "method": "windows",
                "exe": exe,
                "wine": None,
                "message": f"LEWICE executable found ({os.path.basename(exe)}). It will run directly.",
            }
        return {
            "ok": False,
            "method": None,
            "exe": exe,
            "wine": None,
            "message": (
                f"LEWICE executable not found at {exe}. "
                "Place the NASA LEWICE 3.2 lewice.exe in the repository root."
            ),
        }

    wine = shutil.which("wine") or shutil.which("wine64")
    if not os.path.isfile(exe):
        return {
            "ok": False,
            "method": None,
            "exe": exe,
            "wine": wine,
            "message": (
                f"LEWICE executable not found at {exe}. "
                "This app runs the NASA LEWICE 3.2 Windows executable "
                "(lewice.exe in the repository root) and does not embed the solver. "
                "On Linux that executable is started with Wine."
            ),
        }
    if not wine:
        return {
            "ok": False,
            "method": None,
            "exe": exe,
            "wine": None,
            "message": (
                "lewice.exe is present, but Wine is not installed, so LEWICE cannot be "
                "started on this Linux host. Install wine (the Docker image uses wine64 "
                "and wine32) and restart the app. No ice shape will be produced until then."
            ),
        }
    return {
        "ok": True,
        "method": "wine",
        "exe": exe,
        "wine": wine,
        "message": (
            "LEWICE executable found (lewice.exe). On this host it runs through Wine."
        ),
    }


def _write_responses(path, inp_name, xyd_name):
    # One CRLF per line. Doubling the CR (writing \\r\\n under newline='\\r\\n')
    # makes the Fortran runtime reject the filename.
    lines = [inp_name, xyd_name] + ["Y"] * _RESPONSE_LINES
    data = ("\r\n".join(lines) + "\r\n").encode("ascii")
    with open(path, "wb") as f:
        f.write(data)


def _ensure_local_input(src, work_dir, local_name):
    """Copy the namelist and geometry into the work directory under a short name.

    Relative names avoid Wine drive-letter and space problems. The copy is
    skipped when the source is already that file.
    """
    dest = os.path.join(work_dir, local_name)
    src_abs = os.path.abspath(src)
    dest_abs = os.path.abspath(dest)
    if src_abs != dest_abs:
        shutil.copyfile(src_abs, dest_abs)
    return dest


def _tail(text, limit=2500):
    text = text or ""
    if len(text) <= limit:
        return text
    return text[-limit:]


def _run_windows(exe, work_dir, timeout):
    response = os.path.join(work_dir, "responses.txt")
    with open(response, "r", encoding="ascii", errors="replace") as f:
        payload = f.read()
    return subprocess.run(
        [exe],
        input=payload,
        capture_output=True,
        text=True,
        cwd=work_dir,
        timeout=timeout,
    )


def _run_wine(wine, exe, work_dir, timeout):
    bat_path = os.path.join(work_dir, "run_lewice.bat")
    wine_exe = _wine_path(exe)
    # Quote the executable. Inputs are relative to work_dir.
    bat = (
        "@echo off\r\n"
        f"\"{wine_exe}\" < responses.txt > lewice_stdout.txt 2> lewice_stderr.txt\r\n"
        "echo %ERRORLEVEL%> lewice_exitcode.txt\r\n"
    )
    with open(bat_path, "wb") as f:
        f.write(bat.encode("ascii"))
    env = os.environ.copy()
    env.setdefault("WINEDEBUG", "-all")
    completed = subprocess.run(
        [wine, "cmd", "/c", "run_lewice.bat"],
        cwd=work_dir,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    stdout_path = os.path.join(work_dir, "lewice_stdout.txt")
    stderr_path = os.path.join(work_dir, "lewice_stderr.txt")
    code_path = os.path.join(work_dir, "lewice_exitcode.txt")
    stdout = ""
    stderr = ""
    if os.path.isfile(stdout_path):
        with open(stdout_path, "r", errors="replace") as f:
            stdout = f.read()
    if os.path.isfile(stderr_path):
        with open(stderr_path, "r", errors="replace") as f:
            stderr = f.read()
    return_code = completed.returncode
    if os.path.isfile(code_path):
        with open(code_path, "r", errors="replace") as code_f:
            raw = code_f.read().strip()
        try:
            return_code = int(raw)
        except ValueError:
            pass
    completed.stdout = stdout
    completed.stderr = stderr
    completed.returncode = return_code
    return completed


def run_lewice(inp_file, xyd_file, work_dir=None, timeout=300, exe_path=None):
    """Run a single LEWICE case.

    Returns a dict with status, output_dir, elapsed_seconds, stdout, stderr,
    and message. status is "success", "error", or "timeout".

    Success requires a finished final1.dat and no Fortran "severe" abort.
    A missing executable or a missing Wine install returns status "error"
    with a message that says which one is missing.
    """
    probe = probe_lewice(exe_path)
    if not probe["ok"]:
        return {"status": "error", "message": probe["message"], "stdout": "", "stderr": ""}

    if not os.path.isfile(inp_file):
        return {"status": "error", "message": f"LEWICE input file not found: {inp_file}"}
    if not os.path.isfile(xyd_file):
        return {"status": "error", "message": f"Geometry file not found: {xyd_file}"}

    if work_dir is None:
        work_dir = os.path.join(os.path.dirname(os.path.abspath(inp_file)), "run_output")
    os.makedirs(work_dir, exist_ok=True)

    _ensure_local_input(inp_file, work_dir, "case.inp")
    _ensure_local_input(xyd_file, work_dir, "case.xyd")
    _write_responses(os.path.join(work_dir, "responses.txt"), "case.inp", "case.xyd")

    start = time.time()
    try:
        if probe["method"] == "windows":
            completed = _run_windows(probe["exe"], work_dir, timeout)
        else:
            completed = _run_wine(probe["wine"], probe["exe"], work_dir, timeout)
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": (
                f"LEWICE exceeded the {timeout:.0f} s limit for this case and was stopped. "
                "A long exposure is split into more icing steps and takes longer. "
                "Shorten the exposure or run fewer sweep cases."
            ),
            "output_dir": work_dir,
            "elapsed_seconds": round(time.time() - start, 2),
        }
    except OSError as exc:
        return {
            "status": "error",
            "message": f"Could not start LEWICE ({probe['method']}): {exc}",
            "output_dir": work_dir,
        }

    elapsed = round(time.time() - start, 2)
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    stdout_path = os.path.join(work_dir, "lewice_stdout.txt")
    if stdout and not os.path.isfile(stdout_path):
        with open(stdout_path, "w", encoding="utf-8", errors="replace") as log_f:
            log_f.write(stdout)
    final_path = os.path.join(work_dir, "final1.dat")
    severe = "severe" in stderr.lower() or "forrtl" in stderr.lower()
    finished = os.path.isfile(final_path) and os.path.getsize(final_path) > 0 and "Run Time" in stdout

    if finished and not severe and completed.returncode == 0:
        status = "success"
        message = f"LEWICE completed in {elapsed:.1f} s."
    elif finished and not severe:
        # Wine occasionally reports a leftover status even when the log shows
        # a normal "Run Time" line and final1.dat was written.
        status = "success"
        message = f"LEWICE completed in {elapsed:.1f} s (exit code {completed.returncode})."
    else:
        status = "error"
        detail = _tail(stderr.strip() or stdout.strip())
        message = "LEWICE did not finish."
        if severe:
            message = (
                "LEWICE aborted with a Fortran runtime error. "
                "If this says CONOUT$ or 'invalid handle', the executable was started "
                "with a piped console; rerun from LEWICE Studio so it can use a batch console."
            )
        if not os.path.isfile(final_path):
            message += " final1.dat was not written."
        if detail:
            message += "\n\n" + detail

    return {
        "status": status,
        "return_code": completed.returncode,
        "output_dir": work_dir,
        "elapsed_seconds": elapsed,
        "stdout": stdout,
        "stderr": stderr,
        "message": message,
    }


def run_batch(cases, base_output_dir="batch_output"):
    """Run multiple LEWICE cases sequentially.

    Each case dict needs inp_file, xyd_file, and an optional case_name.
    """
    os.makedirs(base_output_dir, exist_ok=True)
    results = []
    total = len(cases)

    for i, case in enumerate(cases):
        case_name = case.get("case_name", f"case_{i + 1:03d}")
        work_dir = os.path.join(base_output_dir, case_name)
        print(f"[{i + 1}/{total}] Running {case_name}...")

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
    info = probe_lewice()
    print(info["message"])
