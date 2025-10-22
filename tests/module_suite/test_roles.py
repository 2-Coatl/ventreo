"""Integration tests for the identity module REST surface."""
from __future__ import annotations

from rest_framework.test import APIClient

from identity.models import Role, RoleBundle
from identity.services import highest_privilege_role


def test_role_listing_returns_seeded_roles() -> None:
    """Roles are exposed through the identity API."""

    RoleBundle.objects.all().delete()
    Role.objects.all().delete()
    Role.objects.bulk_create(
        [
            Role(slug='ceo', name='CEO', hierarchy_level=2, description='Chief executive role.'),
            Role(slug='cfo', name='CFO', hierarchy_level=3, description='Finance lead.'),
        ]
    )
    client = APIClient()
    response = client.get('/api/identity/roles/')
    assert response.status_code == 200
    payload = response.json()
    assert {item['slug'] for item in payload['results']} == {'ceo', 'cfo'}


def test_bundle_endpoint_includes_nested_roles() -> None:
    """Bundles return their assigned roles."""

    RoleBundle.objects.all().delete()
    Role.objects.all().delete()
    ceo = Role.objects.create(slug='ceo', name='CEO', hierarchy_level=2, description='Executive leader')
    cfo = Role.objects.create(slug='cfo', name='CFO', hierarchy_level=3, description='Finance lead')
    bundle = RoleBundle.objects.create(key='small', title='Pequeña empresa', description='Separación CEO/CFO')
    bundle.roles.set([ceo, cfo])

    client = APIClient()
    response = client.get('/api/identity/bundles/')
    assert response.status_code == 200
    payload = response.json()
    first_bundle = payload['results'][0]
    assert first_bundle['roles'][0]['slug'] in {'ceo', 'cfo'}
    assert {role['slug'] for role in first_bundle['roles']} == {'ceo', 'cfo'}


def test_highest_privilege_role_returns_lowest_hierarchy_level() -> None:
    """Service helper returns the role with the smallest hierarchy value."""

    RoleBundle.objects.all().delete()
    Role.objects.all().delete()
    Role.objects.bulk_create(
        [
            Role(slug='viewer', name='Viewer', hierarchy_level=7, description='Lectura únicamente'),
            Role(slug='controller', name='Controller', hierarchy_level=4, description='Control presupuestal'),
            Role(slug='super_admin', name='Super Admin', hierarchy_level=1, description='Acceso total'),
        ]
    )
    highest = highest_privilege_role(['controller', 'viewer', 'super_admin'])
    assert highest is not None
    assert highest.slug == 'super_admin'
