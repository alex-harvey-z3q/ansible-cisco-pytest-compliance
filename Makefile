PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
RUFF := $(VENV)/bin/ruff
ANSIBLE_LINT := $(VENV)/bin/ansible-lint
MOLECULE := $(VENV)/bin/molecule
ANSIBLE_GALAXY := $(VENV)/bin/ansible-galaxy

SCENARIO ?= default

.PHONY: check-cisco-env venv install lint lint-ansible molecule-deps molecule-inventory molecule-prepare molecule-converge molecule-test check clean

check-cisco-env:
	@test -n "$(CISCO_HOST)" || (echo "CISCO_HOST is not set"; exit 1)
	@test -n "$(CISCO_USER)" || (echo "CISCO_USER is not set"; exit 1)
	@test -n "$(CISCO_PASS)" || (echo "CISCO_PASS is not set"; exit 1)

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

install: venv molecule-deps

lint:
	$(RUFF) check .

lint-ansible:
	$(ANSIBLE_LINT) defaults handlers meta tasks vars molecule

molecule-deps:
	$(ANSIBLE_GALAXY) collection install -r collections/requirements.yml

molecule-prepare: check-cisco-env
	$(MOLECULE) prepare -s $(SCENARIO)

molecule-converge: check-cisco-env
	$(MOLECULE) converge -s $(SCENARIO)

molecule-test: check-cisco-env
	$(MOLECULE) test -s $(SCENARIO)

check: lint lint-ansible test

clean:
	rm -rf $(VENV) .pytest_cache .coverage htmlcov .ruff_cache .molecule
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
