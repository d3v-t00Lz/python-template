# Usage
This document describes basic usage of the template repository and it's
tooling.

# Forking
Forking is how you create a new repository from this template.  It will
rename everything to the new project name, and remove components that are not
needed.

See `tools/fork.py --help` for many different options to customize the new
repository.  Note that `tools/fork.py` deletes itself upon completion, as
it would not be viable to run it a 2nd time.  If you wish to create custom
forks of this repository to be forked again, do not use `tools/fork.py` to
remove components.

# Additional tooling
See the `Makefile` for additional tooling that can be used.  `tools/fork.py`
will remove unused Makefile targets depending on the options that were chosen,
so this may vary by repo.

# Creating a new release
Update `${PROJECT_NAME}/__init__.py:__version__`, commit and then tag a new
release with that version.  Package as required.

# Running unit tests
```
make test
# to open the coverage report:
firefox htmlcov/index.html
```

# Vendoring Dependencies
Store packages from pip locally in the project, instead of installing to the
system or venv.

Generally, this is considered a bad practice as it increases
the maintenance burden of enforcing security updates, but
has the advantages of creating stability, and making testing updates
more explicit (no surprises in production because a package was updated
on a host or container image without warning).

Vendoreed packages are stored in `src/pytemplate_vendor/` and can be imported
transparently, as that folder will be added as the first path in `sys.path`.
```
tools/vendor.sh package-name-1 package-name-2
```

# Generating Tab Completion Scripts
This is done with the `install_completions` target in the `Makefile`.  It is
controlled by the `DESTDIR`, `COMPLETIONS_DIR` and `COMPLETIONS_SHELL`
variables.

The RPM and Debian packages already include tab completion scripts.
Unfortunately, `setuptools` makes it difficult to drop files in arbitrary
folders when installing a Python package, so there is no easy, automatic
way to install tab completions directly from pip.  The easiest way is to
add a subcommand to your script that uses shtab to generate a script and
dump it in the users' local tab completion script directory

See the `Makefile` source for more details.

