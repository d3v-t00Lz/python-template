#!/bin/sh -xe

# Developer tools required to build packages

sudo dnf update
sudo dnf install jq pandoc rpm-build python3-devel

