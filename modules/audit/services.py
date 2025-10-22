"""Plain-Python audit log utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class AuditEntry:
    """Single action recorded in the audit log."""

    timestamp: datetime
    user: str
    role: str
    sheet: str
    action: str
    description: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


class AuditLog:
    """In-memory representation of the RBAC audit trail."""

    def __init__(self) -> None:
        self._entries: List[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        """Persist a new entry in the log."""

        self._entries.append(entry)

    def extend(self, entries: Iterable[AuditEntry]) -> None:
        """Add multiple entries at once."""

        self._entries.extend(entries)

    def all(self) -> Sequence[AuditEntry]:
        """Return the immutable view of recorded events."""

        return tuple(self._entries)

    def filter_by_sheet(self, sheet: str) -> Sequence[AuditEntry]:
        """Return entries scoped to a single spreadsheet."""

        return tuple(entry for entry in self._entries if entry.sheet == sheet)

    def filter_by_user(self, user: str) -> Sequence[AuditEntry]:
        """Return entries recorded by the provided identity."""

        return tuple(entry for entry in self._entries if entry.user == user)

    def latest(self) -> AuditEntry | None:
        """Return the last recorded entry if any."""

        return self._entries[-1] if self._entries else None


__all__ = ['AuditEntry', 'AuditLog']
