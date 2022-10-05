#!/bin/bash -xe

cd /src
pyver=$(python3 -c "
import sys
v = sys.version_info
print(f'py{v[0]}{v[1]}')
")
workdir=".test-all-workdir/${pyver}"

if [ ! -d "$workdir" ]; then
	python3 -m venv "$workdir"
fi

export PATH="$(pwd)/${workdir}/bin":"${PATH}"

which python3 \
&& which pip3 \
&& pip3 install \
	-r requirements/devel.txt \
	-r requirements/common.txt \
    -r requirements/cli.txt \
    -r requirements/rest.txt \
    -r requirements/test.txt \
&& PT_EXCLUDE_LIBS=ALL pip3 install -e . \
&& python3 -m pytest

