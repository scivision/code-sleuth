"""
functions used to interface with CMake
"""
import subprocess
import json
import typing as T
from pathlib import Path
import shutil
import pkg_resources
import tempfile
import os


def cmake_ok() -> str:
    exe = shutil.which("cmake")
    if not exe:
        raise FileNotFoundError("CMake not found")

    version = subprocess.check_output([exe, "--version"], universal_newlines=True).split()[2]
    if pkg_resources.parse_version(version) < pkg_resources.parse_version("3.14"):
        raise RuntimeError("CMake >= 3.14 required for CMake-file-api")

    return exe


def cmake_generate(source_dir: Path, build_dir: Path, env: T.Dict[str, str] = None):
    """
    CMake >= 3.13 Generate
    """

    if env is None:
        env = {}

    cmd = ["cmake", "-S", str(source_dir), "-B", str(build_dir)]
    ret = subprocess.run(cmd, env=os.environ.update(env))

    if ret.returncode:
        raise RuntimeError(" ".join(cmd))


def cmake_api(source_dir: Path) -> T.List[str]:
    """
    CMake >= 3.14 has the CMake File API
    https://cmake.org/cmake/help/latest/manual/cmake-file-api.7.html

    We don't use the context manager because of Windows, a well known issue
    """
    tmp = tempfile.TemporaryDirectory()
    build_dir = Path(tmp.name)

    api_dir = build_dir / ".cmake/api/v1"
    query_dir = api_dir / "query"
    query_dir.mkdir(parents=True, exist_ok=True)

    # request CMake Cache info
    (query_dir / "cache-v2").touch()
    (query_dir / "codemodel-v2").touch()

    cmake_generate(source_dir, build_dir)
    resp_dir = api_dir / "reply"
    # retrieve the newest file to get the reply
    index_fn = sorted(resp_dir.glob("index-*.json"), reverse=True)[0]

    index = json.loads(index_fn.read_text())
    codemodel = json.loads(
        (resp_dir / index["reply"]["codemodel-v2"]["jsonFile"]).read_text(errors="ignore")
    )

    # if desired
    # cmake_cache = json.loads((resp_dir / index["reply"]["cache-v2"]["jsonFile"]).read_text(errors="ignore"))
    # cache = {entry["name"]: entry["value"] for entry in cmake_cache["entries"]}

    # info = {}
    # if "CMAKE_GENERATOR" in cache:
    #     info["backend"] = cache["CMAKE_GENERATOR"]

    langs: T.List[str] = []
    for conf in codemodel["configurations"]:
        for targ in conf["targets"]:
            tobj = json.loads((resp_dir / targ["jsonFile"]).read_text(errors="ignore"))
            for cg in tobj["compileGroups"]:
                langs.append(cg["language"])

    try:
        tmp.cleanup()
    except PermissionError:
        pass

    return list(set(langs))
