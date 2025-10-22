"""Tests for the access control matrix backed by Django models."""
from __future__ import annotations

from rest_framework.test import APIClient

from access_control.models import Sheet, SheetPermission
from access_control.services import resolve_sheet_permissions
from identity.models import Role


def test_permissions_endpoint_returns_flags_for_sheet() -> None:
    """The access control API exposes permissions per sheet."""

    SheetPermission.objects.all().delete()
    Sheet.objects.all().delete()
    Role.objects.all().delete()
    cfo = Role.objects.create(slug='cfo', name='CFO', hierarchy_level=3, description='Finance lead')
    sheet = Sheet.objects.create(code='05_Costos_Fijos', title='Costos Fijos', description='Control presupuestal')
    SheetPermission.objects.create(sheet=sheet, role=cfo, can_read=True, can_write=True)

    client = APIClient()
    response = client.get('/api/access-control/sheets/05_Costos_Fijos/')
    assert response.status_code == 200
    payload = response.json()
    assert payload['code'] == '05_Costos_Fijos'
    assert payload['permissions'][0]['can_write'] is True


def test_permission_service_combines_roles() -> None:
    """Service aggregates permissions across roles."""

    SheetPermission.objects.all().delete()
    Sheet.objects.all().delete()
    Role.objects.all().delete()
    sheet = Sheet.objects.create(code='02_Inversion_Inicial', title='Inversión Inicial', description='CapEx approvals')
    cfo = Role.objects.create(slug='cfo', name='CFO', hierarchy_level=3, description='Finance lead')
    ceo = Role.objects.create(slug='ceo', name='CEO', hierarchy_level=2, description='Chief executive')
    SheetPermission.objects.create(sheet=sheet, role=cfo, can_read=True, can_write=True)
    SheetPermission.objects.create(sheet=sheet, role=ceo, can_read=True, can_approve=True)

    combined = resolve_sheet_permissions('02_Inversion_Inicial', ['cfo', 'ceo'])
    assert combined.read is True
    assert combined.write is True
    assert combined.approve is True


def test_unknown_sheet_returns_empty_permission_set() -> None:
    """Unknown sheets fallback to an empty permission set."""

    SheetPermission.objects.all().delete()
    Sheet.objects.all().delete()
    Role.objects.all().delete()
    Role.objects.create(slug='ceo', name='CEO', hierarchy_level=2, description='Chief executive')
    empty = resolve_sheet_permissions('00_Inexistente', ['ceo'])
    assert empty.read is False
    assert empty.write is False
