#! /bin/bash -i
{{ python-executable }} \
	-u "${APPDIR}/opt/python{{ python-version }}/bin/pytemplate_qt" "$@"
