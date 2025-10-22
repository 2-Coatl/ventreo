VENV?=.venv
PYTHON?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip
MANAGE?=$(PYTHON) manage.py

.PHONY: venv install migrate run lint format test shell collectstatic \
securityrat-up securityrat-halt securityrat-destroy securityrat-logs \
securityrat-export

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

SECURITYRAT_DIR?=docs/security/securityrat
SECURITYRAT_CONTAINER?=ventreo-securityrat
SECURITYRAT_EXPORT_DIR?=docs/security/securityrat_exports
SECURITYRAT_EXPORT_PATH?=/opt/securityrat/exports

securityrat-up:
	cd $(SECURITYRAT_DIR) && vagrant up --provider=docker

securityrat-halt:
	cd $(SECURITYRAT_DIR) && vagrant halt

securityrat-destroy:
	cd $(SECURITYRAT_DIR) && vagrant destroy -f

securityrat-logs:
	cd $(SECURITYRAT_DIR) && vagrant docker-logs

securityrat-export:
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	dest=$(SECURITYRAT_EXPORT_DIR)/$$timestamp; \
	echo "Exportando artefactos SecurityRAT a $$dest"; \
	mkdir -p $$dest; \
	command -v docker >/dev/null 2>&1 || { echo 'Docker no está instalado en el host.'; exit 1; }; \
	docker cp $(SECURITYRAT_CONTAINER):$(SECURITYRAT_EXPORT_PATH)/. $$dest
