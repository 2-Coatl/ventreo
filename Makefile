VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip
MANAGE?=$(PYTHON) manage.py

.PHONY: venv install migrate run lint format test shell collectstatic

venv:
	python3.11 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

migrate:
	$(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000

lint:
	$(VENV)/bin/ruff check site authentication

format:
	$(VENV)/bin/black site authentication

collectstatic:
	$(MANAGE) collectstatic --noinput

test:
	$(VENV)/bin/pytest

shell:
	$(MANAGE) shell
