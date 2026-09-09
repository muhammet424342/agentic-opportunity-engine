from __future__ import annotations

from pathlib import Path
from typing import Any

from sibyl_memory_client import MemoryClient

# A tombstoned entry keeps its reason but has lost the payload that used to
# steer a decision, so it can never flip one again.
TOMBSTONE = "tombstoned"

LIVE_STATUSES = {"applied", "submitted", "rejected", "won"}


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
            {"status": status, "reason": reason, "quiet_decisions": 0},
        )
        self.client.write_event(
            acted=f"application:{slug}:{status}",
            extra={"reason": reason},
        )

    def outcome(self, slug: str) -> dict[str, Any] | None:
        """The payload a decision is allowed to read. Tombstones are invisible here."""
        body = self.trail(slug)
        if body is None or body.get("status") == TOMBSTONE:
            return None
        return body

    def trail(self, slug: str) -> dict[str, Any] | None:
        """The raw record, tombstones included. This is the audit view, not the decision view."""
        try:
            return self.client.get_entity("applications", slug)["body"]
        except Exception:
            return None

    def note_decision(self, slug: str, *, flipped: bool) -> None:
        """Advance this entry's clock.

        The clock is decisions, not calendar time: an agent idle for a week has
        not learned that its memory is dead, it has only been asleep. A flip
        proves the entry still earns its place, so it resets the count.
        """
        body = self.trail(slug)
        if body is None or body.get("status") == TOMBSTONE:
            return
        body["quiet_decisions"] = 0 if flipped else int(body.get("quiet_decisions", 0)) + 1
        self.client.set_entity("applications", slug, body)

    def tombstone(self, slug: str) -> bool:
        """Drop the payload, keep the reason. Returns False if there was nothing live to prune."""
        body = self.trail(slug)
        if body is None or body.get("status") == TOMBSTONE:
            return False
        quiet = int(body.get("quiet_decisions", 0))
        self.client.set_entity(
            "applications",
            slug,
            {
                "status": TOMBSTONE,
                "reason": body.get("reason", ""),
                "was": body.get("status", ""),
                "pruned_after": quiet,
            },
        )
        self.client.write_event(
            acted=f"application:{slug}:{TOMBSTONE}",
            extra={"was": body.get("status", ""), "pruned_after": quiet},
        )
        return True

    def prune(self, max_quiet_decisions: int) -> list[str]:
        """Tombstone every entry that has sat through max_quiet_decisions without flipping one."""
        pruned: list[str] = []
        for entity in self.client.list_entities("applications", limit=1000):
            body = entity.get("body") or {}
            if body.get("status") == TOMBSTONE:
                continue
            if int(body.get("quiet_decisions", 0)) >= max_quiet_decisions:
                if self.tombstone(entity["name"]):
                    pruned.append(entity["name"])
        return pruned
