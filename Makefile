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
SECURITYRAT_SERVICE?=securityrat
SECURITYRAT_EXPORT_DIR?=docs/security/securityrat_exports
SECURITYRAT_EXPORT_PATH?=/opt/securityrat/exports

securityrat-up:
	cd $(SECURITYRAT_DIR) && vagrant up --provision

securityrat-halt:
	cd $(SECURITYRAT_DIR) && vagrant halt

securityrat-destroy:
	cd $(SECURITYRAT_DIR) && vagrant destroy -f

securityrat-logs:
	cd $(SECURITYRAT_DIR) && vagrant ssh -c "cd /vagrant/$(SECURITYRAT_DIR) && docker compose logs --tail=200 $(SECURITYRAT_SERVICE)"

securityrat-export:
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	dest=$(SECURITYRAT_EXPORT_DIR)/$$timestamp; \
	echo "Exportando artefactos SecurityRAT a $$dest"; \
	mkdir -p $$dest; \
	cd $(SECURITYRAT_DIR) && \
	vagrant ssh -c "cd /vagrant/$(SECURITYRAT_DIR) && mkdir -p /vagrant/$(SECURITYRAT_EXPORT_DIR)/$$timestamp && docker compose cp $(SECURITYRAT_SERVICE):$(SECURITYRAT_EXPORT_PATH)/. /vagrant/$(SECURITYRAT_EXPORT_DIR)/$$timestamp && chown -R vagrant:vagrant /vagrant/$(SECURITYRAT_EXPORT_DIR)/$$timestamp"
