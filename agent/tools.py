import pathlib
import subprocess
from typing import Optional, Tuple

from langchain_core.tools import tool

PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


def safe_path_for_project(path: str) -> pathlib.Path:
    """
    Ensure all file operations stay within PROJECT_ROOT.
    """
    p = (PROJECT_ROOT / path).resolve()

    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to access outside project root")

    return p


@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file inside the project root.
    """
    p = safe_path_for_project(path)

    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"WROTE:{p}"


@tool
def read_file(path: str) -> str:
    """
    Reads content from a file inside the project root.
    """
    p = safe_path_for_project(path)

    if not p.exists():
        return ""

    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
def get_current_directory() -> str:
    """
    Returns the project root directory.
    """
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """
    Lists all files recursively within a directory.
    """
    p = safe_path_for_project(directory)

    if not p.is_dir():
        return f"ERROR: {p} is not a directory"

    files = [
        str(f.relative_to(PROJECT_ROOT))
        for f in p.glob("**/*")
        if f.is_file()
    ]

    return "\n".join(files) if files else "No files found."


@tool
def run_cmd(
    cmd: str,
    cwd: Optional[str] = None,
    timeout: int = 30
) -> Tuple[int, str, str]:
    """
    Runs a shell command and returns:
    (return_code, stdout, stderr)
    """
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return (
            result.returncode,
            result.stdout,
            result.stderr,
        )

    except subprocess.TimeoutExpired:
        return (
            1,
            "",
            f"Command timed out after {timeout} seconds",
        )


def init_project_root() -> str:
    """
    Creates the project root directory if it doesn't exist.
    """
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)

