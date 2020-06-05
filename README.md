# code-sleuth

![ci](https://github.com/scivision/code-sleuth/workflows/ci/badge.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/code-sleuth.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/code-sleuth/context:python)

Current status: prototype

---

Actively discover the primary coding languages of projects via deep introspection where necessary.
First, Code Sleuth looks at known metadata such as codemeta.json to determine primary project languages.
This approach scales to millions of projects.

Next, lightweight heuristics are considers such as presence of language-specific configuration files.
It is thought that Makefiles might lend themselves to passive heuristics.

If metadata is not usable and lightweight heuristics are indeterminate, Code Sleuth enters deep introspection by configuring the project build system.
Currently, deep introspection only occurs for CMake-based projects.
The introspection method extends in a straightforward way to Meson in the future.


Introspection is **not safe** for the running computer, because executing build scripts can (over)write arbitrary files and Windows Registry.
This script is meant to be run on "known safe" projects or as a cloud instance that is OK with the risk of running scripts from any project on the Internet.


The purpose of the deep introspection method is to acquire language standard data on thousands of scientific computing projects, where a throwaway cloud image would be used for the scanning.
The deep introspection would take place infrequently after the first project scan, and could take a minute or more of single-CPU time per project.

We provide initial implementation of a tool code-sleuth that actively introspects projects, using a variety of heuristics and direct action.
A key design factor of code-sleuth is to introspect languages using specific techniques such as invoking CMake or Meson to introspect the project developers intended languages.
The goal is not to detect every language in a project, but instead to detect the primary languages of a project.
Also, we desire to resolve the language standards required, for example:

* Python 2.6..2.7
* Python > 3.6
* C++14
* C11
* Fortran 2008

This detection will allow a user to know what compiler or environment is needed in automated fashion.
