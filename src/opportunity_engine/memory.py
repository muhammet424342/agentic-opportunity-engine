from __future__ import annotations

from pathlib import Path
from typing import Any

from sibyl_memory_client import MemoryClient


class OpportunityMemory:
    """Durable decision state backed by the official Sibyl Memory client."""

    def __init__(self, db_path: str | Path, tenant_id: str = "opportunity-engine"):
        self.client = MemoryClient.local(str(db_path), tenant_id=tenant_id)

    def remember_profile(self, *, skills: list[str], preferred_tags: list[str]) -> None:
        self.client.set_entity(
            "profiles",
            "active-builder",
            {"skills": skills, "preferred_tags": preferred_tags},
        )

    def profile(self) -> dict[str, Any]:
        try:
            return self.client.get_entity("profiles", "active-builder")["body"]
        except Exception:
            return {"skills": [], "preferred_tags": []}

    def remember_outcome(self, slug: str, status: str, reason: str = "") -> None:
        self.client.set_entity(
            "applications",
            slug,
            {"status": status, "reason": reason},
        )
        self.client.write_event(
            acted=f"application:{slug}:{status}",
            extra={"reason": reason},
        )

    def outcome(self, slug: str) -> dict[str, Any] | None:
        try:
            return self.client.get_entity("applications", slug)["body"]
        except Exception:
            return None
