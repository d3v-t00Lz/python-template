ORG ?= $(shell jq .org meta.json)
PRODUCT ?= $(shell jq -r .product meta.json)
VERSION ?= $(shell grep __version__ pytemplate/__init__.py | grep -oE "([0-9]+\.[0-9]+\.[0-9]+)")
DOCKER ?= podman
DOCKER_TAG ?= $(ORG)/$(PRODUCT)
COMPLETIONS_DIR ?= /usr/share/bash-completions/completions
COMPLETIONS_SHELL ?= bash
DESTDIR ?=
PREFIX ?= /usr

.PHONY: test

clean:
	# Remove temporary build files
	rm -rf build/ dist/ htmlcov/ *.egg-info *.nsi .pytest_cache/ \
		./.rpmbuild/ *.rpm *.deb
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
	dpkg-deb --build --root-owner-group . $(PRODUCT)-$(VERSION)-noarch.deb

install_completions:
	# Generate UNIX shell completion scripts so the user can tab-complete
	# commands
	install -d $(DESTDIR)$(COMPLETIONS_DIR)
	python3 $(shell which shtab) \
		--shell=$(COMPLETIONS_SHELL) \
		--prog pytemplate \
		-u pytemplate_cli.args.arg_parser \
		| tee $(DESTDIR)/$(COMPLETIONS_DIR)/$(PRODUCT)

install_linux: \
	# Install various files for Linux,
	# `setup.py install` must be run separately
	install_completions \
	install_linux_icon \
	install_linux_vendor \
	install_systemd

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

pdb:
	# Debug unit tests that raise Exceptions with PDB
	pytest --pdb

pypi: test type-check
	# Upload your package to PyPi so that anybody can install using pip.
	# Requires `twine` to be installed, and a local twine config with your
	# pypi username and password
	rm -rf dist/*
	python3 setup.py sdist
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
		rpm.spec
	cp ./.rpmbuild/RPMS/noarch/*$(PRODUCT)-$(VERSION)*.rpm .

test:
	# Run the unit tests
	./setup.py test

type-check:
	# Check typing of Python type hints
	mypy --ignore-missing-imports pytemplate pytemplate_cli pytemplate_rest

