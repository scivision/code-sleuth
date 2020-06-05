#!/usr/bin/env python3
"""
CLI for Code Sleuth
"""
import argparse
from pathlib import Path
import typing as T

from .detect import detect_lang
from .cmake import cmake_api


def code_sleuth():
    p = argparse.ArgumentParser(
        description="Code Sleuth: introspect language and standard of projects"
    )
    p.add_argument("source_dir", help="top level directory of project")
    p = p.parse_args()

    source_dir = Path(p.source_dir)

    # %% 1. look for codemeta.json
    print_result(detect_lang(p.source_dir), source_dir)

    # %% 2. look for CMake and introspect
    print_result(cmake_api(source_dir), source_dir)

    raise SystemExit(f"Could not determine langauges: {p.source_dir}")


def print_result(langs: T.Sequence[str], source_dir: Path):
    if not langs:
        return None

    langs = list(set([L.lower() for L in langs]))

    langs = [L.replace("cxx", "c++").replace("cpp", "c++") for L in langs]

    print(source_dir, langs)
    raise SystemExit(0)


if __name__ == "__main__":
    code_sleuth()
