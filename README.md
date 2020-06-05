# code-sleuth

![ci](https://github.com/scivision/code-sleuth/workflows/ci/badge.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/code-sleuth.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/code-sleuth/context:python)

Current status: conceptual

Next step: based on introspection code from our BuildMC project, use CMake and Meson to extract primary code language from projects.

---

Actively discover the primary coding languages of projects via introspection.

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
