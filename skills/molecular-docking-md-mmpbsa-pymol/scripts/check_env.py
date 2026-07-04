#!/usr/bin/env python3
"""Check the molecular docking/MD/MMPBSA software environment."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


EXECUTABLES = {
    "gmx": ["gmx", "gmx_mpi"],
    "vina": ["vina"],
    "obabel": ["obabel"],
    "pymol": ["pymol"],
    "plip": ["plip"],
    "antechamber": ["antechamber"],
    "parmchk2": ["parmchk2"],
    "tleap": ["tleap"],
    "acpype": ["acpype"],
    "gmx_MMPBSA": ["gmx_MMPBSA"],
}

VERSION_ARGS = {
    "gmx": ["--version"],
    "vina": ["--version"],
    "obabel": ["-V"],
    "pymol": ["-cq", "-d", "print(cmd.get_version()[0]); quit"],
    "plip": ["--version"],
    "antechamber": ["-h"],
    "parmchk2": ["-h"],
    "tleap": ["-h"],
    "acpype": ["--version"],
    "gmx_MMPBSA": ["--version"],
}

PYTHON_PACKAGES = {
    "rdkit": "rdkit",
    "MDAnalysis": "MDAnalysis",
    "mdtraj": "mdtraj",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "parmed": "parmed",
    "prolif": "prolif",
    "networkx": "networkx",
    "svgwrite": "svgwrite",
    "cairosvg": "cairosvg",
    "pillow": "PIL",
}

OPTIONAL_EXECUTABLES = {
    "Schrodinger maestro": ["maestro"],
    "Schrodinger run": ["run"],
    "Schrodinger structconvert": ["structconvert"],
    "Schrodinger prepwizard": ["prepwizard"],
}


@dataclass
class CheckResult:
    name: str
    installed: bool
    path: str = ""
    version: str = ""
    detail: str = ""


def short_output(text: str, max_lines: int = 3) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " | ".join(lines[:max_lines])


def probe_version(name: str, executable: str) -> str:
    args = VERSION_ARGS.get(name)
    if not args:
        return ""
    try:
        proc = subprocess.run(
            [executable, *args],
            text=True,
            capture_output=True,
            timeout=12,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - environment dependent
        return f"version probe failed: {exc}"
    output = short_output(proc.stdout) or short_output(proc.stderr)
    return output


def check_executable(name: str, candidates: list[str]) -> CheckResult:
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return CheckResult(
                name=name,
                installed=True,
                path=path,
                version=probe_version(name, path),
            )
    return CheckResult(
        name=name,
        installed=False,
        detail=f"not found in PATH; tried: {', '.join(candidates)}",
    )


def check_package(display: str, module: str) -> CheckResult:
    spec = importlib.util.find_spec(module)
    if not spec:
        return CheckResult(display, False, detail=f"Python module '{module}' not importable")
    version = ""
    try:
        imported = __import__(module)
        version = str(getattr(imported, "__version__", ""))
    except Exception as exc:  # pragma: no cover - import side effects vary
        version = f"importable; version unavailable: {exc}"
    return CheckResult(display, True, path=str(spec.origin or ""), version=version)


def check_schrodinger_optional() -> list[CheckResult]:
    results = [check_executable(name, candidates) for name, candidates in OPTIONAL_EXECUTABLES.items()]
    env_path = os.environ.get("SCHRODINGER", "")
    if env_path:
        results.insert(0, CheckResult("SCHRODINGER env", True, path=env_path, detail="optional licensed route detected"))
    else:
        results.insert(0, CheckResult("SCHRODINGER env", False, detail="not set; optional licensed route unavailable"))
    return results


def print_table(title: str, rows: list[CheckResult]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for row in rows:
        status = "OK" if row.installed else "MISSING"
        extra = row.version or row.detail or row.path
        print(f"{status:8} {row.name:14} {extra}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if anything is missing.")
    args = parser.parse_args()

    exe_results = [check_executable(name, candidates) for name, candidates in EXECUTABLES.items()]
    pkg_results = [check_package(name, module) for name, module in PYTHON_PACKAGES.items()]
    optional_results = check_schrodinger_optional()
    all_results = exe_results + pkg_results

    if args.json:
        print(json.dumps({"required": [asdict(row) for row in all_results], "optional": [asdict(row) for row in optional_results]}, indent=2))
    else:
        print(f"Python executable: {sys.executable}")
        print(f"Current directory: {Path.cwd()}")
        print_table("Command-line tools", exe_results)
        print_table("Python packages", pkg_results)
        print_table("Optional Schrodinger/Maestro route", optional_results)
        print("\nSchrodinger/Maestro is checked only as an optional licensed route. This skill does not depend on it and will not bypass commercial licensing.")
        missing = [row.name for row in all_results if not row.installed]
        if missing:
            print("\nMissing dependencies:")
            print(", ".join(missing))
            print("\nInstall with:")
            print("mamba env create -f environment.yml")
            print("conda activate mol-mmpbsa")
            print("\nIf mamba is unavailable:")
            print("conda env create -f environment.yml")
            print("conda activate mol-mmpbsa")
            print("\nIf ProLIF is unavailable from conda in your platform, install it after activation:")
            print("pip install prolif")
        else:
            print("\nAll requested tools and Python packages were found.")

    if args.strict and any(not row.installed for row in all_results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
