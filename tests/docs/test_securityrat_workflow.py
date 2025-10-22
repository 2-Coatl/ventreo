"""Tests that cover the SecurityRAT helper environment configuration."""
from __future__ import annotations

import subprocess
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


def _run_make_target(target: str) -> str:
    completed = subprocess.run(
        ["make", "-n", target],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def test_makefile_targets_use_vagrant_and_compose():
    up_output = _run_make_target("securityrat-up")
    logs_output = _run_make_target("securityrat-logs")
    export_output = _run_make_target("securityrat-export")

    assert "cd docs/security/securityrat && vagrant up --provision" in up_output
    assert (
        "cd docs/security/securityrat && vagrant ssh -c \"cd /vagrant/docs/security/securityrat"
        in logs_output
    )
    assert "docker compose logs --tail=200 securityrat\"" in logs_output

    assert "Exportando artefactos SecurityRAT" in export_output
    assert "vagrant ssh -c \"cd /vagrant/docs/security/securityrat" in export_output
    assert "docker compose cp securityrat:/opt/securityrat/exports/." in export_output
    assert "chown -R vagrant:vagrant" in export_output


def test_securityrat_doc_describes_use_case_implementation():
    guide = (REPO_ROOT / "docs/security/securityrat.md").read_text(encoding="utf-8")

    assert "### 4.1 Implementación operativa de los casos de uso" in guide
    assert "Crear un requerimiento base" in guide
    assert "docs/use_cases/UC-0XX-*.md" in guide
    assert "make securityrat-export" in guide
