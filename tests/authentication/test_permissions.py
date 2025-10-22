"""Tests for custom authentication permissions."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import pytest

# Skip the suite when Django REST Framework is unavailable.
pytest.importorskip('rest_framework')

# Ensure the project root is on the import path when running via pytest.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from authentication.permissions import CallCenterPermission


@dataclass
class StubUser:
    """Simple stand-in for Django's user model."""

    is_authenticated: bool


@dataclass
class StubRequest:
    """Simple request object exposing the fields the permission reads."""

    method: str
    user: StubUser


@pytest.mark.parametrize(
    "method", ['GET', 'HEAD', 'OPTIONS'],
)
def test_safe_methods_allow_anonymous_access(method: str) -> None:
    """Anonymous users can perform safe (read-only) operations."""

    request = StubRequest(method=method, user=StubUser(is_authenticated=False))
    permission = CallCenterPermission()

    assert permission.has_permission(request, view=None) is True


@pytest.mark.parametrize(
    "method", ['POST', 'PUT', 'PATCH', 'DELETE'],
)
def test_unsafe_methods_require_authenticated_user(method: str) -> None:
    """Write operations require authentication."""

    request = StubRequest(method=method, user=StubUser(is_authenticated=False))
    permission = CallCenterPermission()

    assert permission.has_permission(request, view=None) is False


def test_authenticated_user_can_perform_write_operations() -> None:
    """Authenticated users are authorised to perform write operations."""

    request = StubRequest(method='POST', user=StubUser(is_authenticated=True))
    permission = CallCenterPermission()

    assert permission.has_permission(request, view=None) is True
