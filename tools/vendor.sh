#!/bin/sh -e

DIRNAME="src/pytemplate_vendor"
USAGE="
Vendor dependencies in ${DIRNAME}

Usage:
tools/vendor.sh [--pip-args...] pypi-package-name1 [pypi-package-name2...]
"

case "$1" in
	-h|--help) echo "$USAGE"; exit 0;;
esac

cd "$(dirname -- ${BASH_SOURCE[0]:-${0:A:h}})/.."
pwd


if [ ! -d "${DIRNAME?}" ]; then
    mkdir "${DIRNAME?}"
fi

if [ ! -f "${DIRNAME?}/__init__.py" ]; then
    touch "${DIRNAME?}/__init__.py"
fi

set -x

pip3 install \
    --ignore-installed \
    --upgrade \
    --target="./${DIRNAME}" \
    "$@"

