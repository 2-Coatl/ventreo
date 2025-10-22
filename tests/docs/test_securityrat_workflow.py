"""Tests that cover the SecurityRAT helper environment configuration."""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_vagrantfile_provisions_docker_compose():
    vagrantfile = (REPO_ROOT / "docs/security/securityrat/Vagrantfile").read_text(encoding="utf-8")

    assert "config.vm.box = ENV.fetch('SECURITYRAT_VAGRANT_BOX', 'bento/ubuntu-22.04')" in vagrantfile
    assert "apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin" in vagrantfile
    assert "docker compose pull || true" in vagrantfile
    assert "docker compose up -d --build" in vagrantfile


def test_docker_compose_exports_shared_volume():
    compose = (REPO_ROOT / "docs/security/securityrat/docker-compose.yml").read_text(encoding="utf-8")

    assert "container_name: ventreo-securityrat" in compose
    assert "../securityrat_exports:/opt/securityrat/exports" in compose
    assert "JAVA_OPTS: ${SECURITYRAT_JAVA_OPTS:-\"-Xms256m -Xmx768m\"}" in compose
    assert "build:" in compose and "dockerfile: Dockerfile" in compose


def test_makefile_targets_use_vagrant_and_compose():
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")

    assert "securityrat-up:" in makefile and "vagrant up --provision" in makefile
    assert "securityrat-logs:" in makefile and "docker compose logs --tail=200 $(SECURITYRAT_SERVICE)" in makefile
    assert "securityrat-export:" in makefile
    assert "docker compose cp $(SECURITYRAT_SERVICE):$(SECURITYRAT_EXPORT_PATH)/." in makefile
    assert "mkdir -p /vagrant/$(SECURITYRAT_EXPORT_DIR)/$$timestamp" in makefile
