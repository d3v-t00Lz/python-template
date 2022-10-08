# Build System
This document describes the build system, the rationale behind it, and
alternatives that have been considered.

# Current System
The current system makes use of `setuptools` for building, configured by
`setup.py`, `setup.cfg` and a minimal `pyproject.toml`.  All tooling is
created without the use of deprecated setup.py CLI commands.

## Rationale
### pyproject.toml
At the time of this writing (2022), the (now 6 years old) `pyproject.toml`
ecosystem is still not mature.  There are bugs such as `pip` failing to
properly isolate from system `setuptools`, introducing bugs such as being
unable to read the version string from `pyproject.toml`.  As such, it is
only used minimally.

### setup.py
`setup.py` should not be invoked directly, however it is still the primary
source of truth for configuring `setuptools`, and all dynamic configuration.
For the simple reason that is `just works`, pretty much all the time on every
system.  There are multiple feature branches open experimenting with ways to
minimze the influence of `setup.py`, but all of them introduce regressions.

# Alternatives
## All-in on pyproject.toml
The current blockers:
- `version` cannot be read dynamically from code by `pyproject.toml`, nor can
  `pkg_resources` read it from `pyproject.toml`.  It always returns `0.0.0`.
  I suspect that it would work on some systems, but I also suspect that it will
  not work on most systems, including mine.  Supposedly the next pip release
  fixes this.
- Setting scripts in `pyproject.toml` does not work

## Poetry
Currently a work in progress, experimental.  But it does not seem to solve the
problems either.

