ORG ?= $(shell jq -r .org meta.json)
PRODUCT ?= $(shell jq -r .product meta.json)
VERSION ?= $(shell grep __version__ src/pytemplate/__init__.py | grep -oE "([0-9]+\.[0-9]+\.[0-9]+)")
DESTDIR ?=
PREFIX ?= /usr

DOCKER ?= podman
DOCKER_TAG ?= $(ORG)/$(PRODUCT)

COMPLETIONS_DIR ?= /usr/share/bash-completion/completions
_COMPLETIONS_DIR ?= $(DESTDIR)/usr/share/bash-completions/completions
COMPLETIONS_EXT ?=
COMPLETIONS_SHELL ?= bash

LINUX_APPLICATIONS_DIR ?= $(DESTDIR)/usr/share/applications
UI ?= qt

.PHONY: test venv

clean:
	# Remove temporary build files
	rm -rf build/ dist/ htmlcov/ ./*.egg-info ./*.nsi .pytest_cache/ \
		./.rpmbuild/ ./*.rpm ./*.deb
	find test/ pytemplate* -name __pycache__ -type d \
		-exec rm -rf {} \; 2>/dev/null \
		|| true

docker-cli: test type-check
	# Build the Docker image for the CLI
	$(DOCKER) build -f Dockerfile-cli -t $(DOCKER_TAG)-cli .

docker-rest: test type-check
	# Build the Docker image for the REST API
	$(DOCKER) build -f Dockerfile-rest -t $(DOCKER_TAG)-rest .

deb: test type-check
	# Build the Debian package
	LINUX_APPLICATIONS_DIR=. UI=qt make install_linux_desktop
	LINUX_APPLICATIONS_DIR=. UI=sdl2 make install_linux_desktop
	_COMPLETIONS_DIR=. COMPLETIONS_EXT=.completions \
		make install_completions
	tar \
		--exclude='__pycache__' \
		--exclude='venv' \
		--exclude='.[^/]*' \
		--exclude='*.tar.*' \
		--transform 's,^\.,$(PRODUCT)-$(VERSION),' \
		-czvf \
		../python3-$(PRODUCT)_$(VERSION).orig.tar.gz \
		./
	DEB_BUILD_OPTIONS=nocheck debuild -i
	rm ../*.orig ../python3-$(PRODUCT)* debian/*debhelper*

git-hooks:
	# Install git hooks for this repository to enable running tests before
	# committing, etc...
	cp -f tools/git-hooks/* .git/hooks/

install_completions:
	# Generate UNIX shell completion scripts so the user can tab-complete
	# commands
	install -d $(_COMPLETIONS_DIR)
	python3 $(shell which shtab) \
		--shell=$(COMPLETIONS_SHELL) \
		--prog pytemplate \
		-u pytemplate_cli.args.arg_parser \
		| tee $(_COMPLETIONS_DIR)/$(PRODUCT)$(COMPLETIONS_EXT)

install_linux: \
	install_completions \
	install_linux_icon \
	install_linux_vendor \
	install_systemd \
	# Install various files for Linux,
	# `pip install .` must be run separately

install_linux_icon:
	# Install the icon files on Linux
	install -d $(DESTDIR)/$(PREFIX)/share/applications
	install -d $(DESTDIR)/$(PREFIX)/share/pixmaps
	install -m 0644 \
		files/icons/$(PRODUCT).png \
		$(DESTDIR)/$(PREFIX)/share/pixmaps/

install_linux_vendor:
	# Install vendored dependencies from pip on Linux
	if [ -d "vendor" ]; then \
		install -d $(DESTDIR)/usr/lib/$(PRODUCT) ; \
		cp -r vendor/ $(DESTDIR)/usr/lib/$(PRODUCT)/ ; \
	fi

install_systemd:
	# Install systemd service file on Linux or other UNIXes that use systemd
	install -d $(DESTDIR)/usr/lib/systemd/system
	install -m 0644 \
		files/linux/systemd.service\
		$(DESTDIR)/usr/lib/systemd/system/$(PRODUCT).service

install_linux_desktop:
	touch "$(LINUX_APPLICATIONS_DIR)/$(PRODUCT)_$(UI).desktop"
	desktop-file-install                                        \
		--set-name="$(PRODUCT)"                             \
		--set-icon="$(PRODUCT)"                             \
		--set-key="Exec" --set-value='$(PRODUCT)_$(UI) %U'  \
		--add-category="Graphics"                           \
		--set-key="Type" --set-value="Application"          \
		--delete-original                                   \
		--dir="$(LINUX_APPLICATIONS_DIR)"                   \
		"$(LINUX_APPLICATIONS_DIR)/$(PRODUCT)_$(UI).desktop"

pdb:
	# Debug unit tests that raise Exceptions with PDB
	pytest --pdb

pypi: test type-check
	# Upload your package to PyPi so that anybody can install using pip.
	# Requires `twine` to be installed, and a local twine config with your
	# pypi username and password
	rm -rf dist/*.tar.gz dist/*.whl
	python3 -m build
	twine upload dist/*

rpm: test type-check
	# Build the RPM package locally in .rpmbuild
	mkdir -p .rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
	tar \
		--exclude='./venv' --exclude='.[^/]*' \
		--transform 's,^\.,$(PRODUCT)-$(VERSION),' \
		-czvf \
		./.rpmbuild/SOURCES/$(PRODUCT)-$(VERSION).tar.gz \
		./
	rpmbuild -v -ba \
		--define "_topdir $(shell pwd)/.rpmbuild" \
		--define "_tmppath $(shell pwd)/.rpmbuild/tmp"\
		tools/rpm.spec
	cp ./.rpmbuild/RPMS/noarch/*$(PRODUCT)-$(VERSION)*.rpm .

test:
	# Run the unit tests
	tox -e $(shell python3 -c "import sys; v = sys.version_info; print(f'py{v[0]}{v[1]}')")

type-check:
	# Check typing of Python type hints
	mypy --ignore-missing-imports \
		src/pytemplate src/pytemplate_cli src/pytemplate_rest

venv:
	# Create a Python "virtual environment" aka venv
	# Run this target before running:
	#     source venv/bin/activate
	#     pip3 install -e .
	python3 -m venv --system-site-packages venv

override_dh_auto_build:
	# Debian shenanigans

override_dh_auto_install:
	# Debian shenanigans
