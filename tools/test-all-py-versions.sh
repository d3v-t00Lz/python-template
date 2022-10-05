#!/bin/sh -xe

DOCKER=podman

cd "$(dirname -- ${BASH_SOURCE[0]:-${0:A:h}})/.."
pwd

for version in {7,8,9,10}; do
	$DOCKER run \
		-v ".:/src" \
		-e pyversion="py3${version}" \
		--entrypoint 'sh' \
		python:3.${version}-bullseye "/src/tools/test-all-helper.sh"
done

echo 'Finished!'
