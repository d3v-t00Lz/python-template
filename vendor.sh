#!/bin/sh -xe

# Usage:
# ./vendor.sh [--pip-args...] pypi-package-name1 [pypi-package-name2...]

DIRNAME="vendor"

if [ ! -d "${DIRNAME?}" ]; then
    mkdir "${DIRNAME?}"
fi

if [ ! -f "${DIRNAME?}/__init__.py" ]; then
    touch "${DIRNAME?}/__init__.py"
fi

pip3 install \
    --ignore-installed \
    --upgrade \
    --target="./${DIRNAME}" \
    "$@"

