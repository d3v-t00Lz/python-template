ORG ?= $(shell jq -r .org meta.json)
PRODUCT ?= $(shell jq -r .product meta.json)
VERSION ?= $(shell grep __version__ src/pytemplate/__init__.py | grep -oE "([0-9]+\.[0-9]+\.[0-9]+)")
DESTDIR ?=
PREFIX ?= /usr

DOCKER ?= podman
DOCKER_TAG ?= $(ORG)/$(PRODUCT)

COMPLETIONS_DIR ?= $(PREFIX)/share/bash-completion/completions
_COMPLETIONS_DIR ?= $(DESTDIR)/$(PREFIX)/share/bash-completions/completions
COMPLETIONS_EXT ?=
COMPLETIONS_SHELL ?= bash

MAN_DIR ?= $(PREFIX)/share/man
SYSTEMD_DIR ?= $(PREFIX)/lib/systemd/system

LINUX_APPLICATIONS_DIR ?= $(DESTDIR)/$(PREFIX)/share/applications
UI ?= qt

.PHONY: requirements test venv

appimage-cli:
	# Build the AppImage for the cli
	./appimage/release.py cli

appimage-qt:
	# Build the AppImage for the Qt UI
	./appimage/release.py qt

appimage-sdl2:
	# Build the AppImage for the SDL2 UI
	./appimage/release.py sdl2

clean:
	# Remove temporary build files
	rm -rf build/ dist/ htmlcov/ ./*.egg-info ./*.nsi .pytest_cache/ \
		./.rpmbuild/ ./*.rpm ./*.deb
	find test/ src/ -name __pycache__ -type d \
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
	install_man_page\
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
		install -d $(DESTDIR)/$(PREFIX)/lib/$(PRODUCT) ; \
		cp -r vendor/ $(DESTDIR)/$(PREFIX)/lib/$(PRODUCT)/ ; \
	fi

install_man_page:
	install -d $(DESTDIR)/$(MAN_DIR)
	cp files/linux/manpage $(PRODUCT).1
	gzip $(PRODUCT).1
	install -m 0644 $(PRODUCT).1.gz $(DESTDIR)/$(MAN_DIR)/
	rm $(PRODUCT).1.gz

install_systemd:
	# Install systemd service file on Linux or other UNIXes that use systemd
	install -d $(DESTDIR)/$(SYSTEMD_DIR)
	install -m 0644 \
		files/linux/systemd.service\
		$(DESTDIR)/$(SYSTEMD_DIR)/$(PRODUCT).service

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

manpage-from-argparse:
	# Generate a man page file.  Must be committed back to git
	# Run this everytime you make changes to the the ArgumentParser
	# Note that this will overwrite any changes you made by hand
	argparse-manpage \
		--pyfile src/pytemplate_cli/args.py \
		--function arg_parser \
		--prog pytemplate_cli \
		--project-name pytemplate \
		--output files/linux/manpage

markdown-from-manpage:
	# Create a markdown document that is easier to edit that the troff/groff
	# format that man pages use.  Must have pandoc installed
	pandoc \
		-f man \
		-t markdown \
		-o files/linux/manpage.md \
		files/linux/manpage

manpage-from-markdown:
	pandoc \
		--standalone \
		-f markdown \
		-t man \
		-o files/linux/manpage \
		files/linux/manpage.md

# TODO: Replace test-all-tox with test-all-docker if using a system that
# does not supply every needed Python version
pypi: test-all-tox type-check
	# Upload your package to PyPi so that anybody can install using pip.
	# Requires `twine` to be installed, and a ~/.pypirc config with your
	# pypi username and password
	rm -rf dist/*.tar.gz dist/*.whl
	python3 -m build
	python3 -m twine upload dist/*

requirements:
	# Install all Python dependencies from pypi/pip
	for x in requirements/*; do pip install -r $${x}; done

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
	#tox -e $(shell python3 -c "import sys; v = sys.version_info; print(f'py{v[0]}{v[1]}')")
	python3 -m pytest

test-all-docker:
	# Test against all versions of Python supported by this code using Docker
	tools/test-all-py-versions.sh $(DOCKER)

test-all-tox:
	# Test against all versions of Python supported by this code using tox
	# This only works if every supported version of Python is installed on
	# this computer
	tox

test-pdb:
	# Debug unit tests that raise Exceptions with PDB
	python3 -m pytest --pdb

type-check:
	# Check typing of Python type hints
	mypy --ignore-missing-imports \
		src/pytemplate \
		src/pytemplate_cli \
		src/pytemplate_rest \

venv:
	# Create a Python "virtual environment" aka venv
	# Run this target before running:
	#     source venv/bin/activate
	#     pip3 install -e .
	python3 -m venv venv

override_dh_auto_build:
	# Debian shenanigans

override_dh_auto_install:
	# Debian shenanigans

