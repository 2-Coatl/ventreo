"""Configure Django for pytest without relying on pytest-django."""
from __future__ import annotations

import os

import django
from django.core.management import call_command

import site_bootstrap  # noqa: F401  Ensures the ``site`` package is project-specific.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site.settings')
django.setup()
call_command('migrate', run_syncdb=True, verbosity=0)
