#!/bin/sh -xe

# Helper script called by:
#     make test-all
# Spawn a Docker container from the official Python images for earch
# version of Python that your application supports, and run the unit tests
# to ensure compatibility with each Python version

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
