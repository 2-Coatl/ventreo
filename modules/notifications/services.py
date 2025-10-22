"""Notification services leveraging the ORM."""
from __future__ import annotations

from typing import Iterable, Sequence

from .models import AlertRule


def recipients_by_severity(severity: str) -> Sequence[str]:
    """Return role slugs targeted by rules of the provided severity."""

    rules = AlertRule.objects.filter(severity=severity).prefetch_related('audience')
    recipients: list[str] = []
    for rule in rules:
        for role in rule.audience.all():
            if role.slug not in recipients:
                recipients.append(role.slug)
    return tuple(recipients)


def rules_for_roles(role_slugs: Iterable[str]) -> list[AlertRule]:
    """Return rules whose audience includes any of the provided roles."""

    return list(AlertRule.objects.filter(audience__slug__in=list(role_slugs)).distinct())


__all__ = ['recipients_by_severity', 'rules_for_roles']
