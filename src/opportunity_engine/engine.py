from __future__ import annotations

from typing import Any

from .memory import OpportunityMemory
from .models import Decision, Opportunity


class OpportunityEngine:
    def __init__(self, memory: OpportunityMemory):
        self.memory = memory

    def _evaluate(
        self, opportunity: Opportunity, outcome: dict[str, Any] | None
    ) -> Decision:
        profile = self.memory.profile()
        preferred = set(profile.get("preferred_tags", []))
        skills = set(profile.get("skills", []))
        reasons: list[str] = []

        if outcome and outcome.get("status") in {"applied", "submitted", "won"}:
            return Decision(
                opportunity.slug,
                opportunity.name,
                0,
                "skip",
                (f"Sibyl recalled prior status: {outcome['status']}",),
            )

        score = min(40, opportunity.reward_usd // 250)
        tag_matches = preferred.intersection(opportunity.tags)
        skill_matches = skills.intersection(opportunity.requirements)
        score += min(35, len(tag_matches) * 12)
        score += min(25, len(skill_matches) * 10)

        if tag_matches:
            reasons.append("preferred stack: " + ", ".join(sorted(tag_matches)))
        if skill_matches:
            reasons.append("verified skills: " + ", ".join(sorted(skill_matches)))
        if outcome and outcome.get("status") == "rejected":
            score = max(0, score - 25)
            reasons.append("past rejection recalled: " + outcome.get("reason", "unknown"))

        score = min(100, score)
        action = "apply" if score >= 55 else "review" if score >= 35 else "skip"
        return Decision(opportunity.slug, opportunity.name, score, action, tuple(reasons))

    def decide(self, opportunity: Opportunity) -> Decision:
        """Decide, and record whether memory actually changed the answer.

        The blind pass is the control: if the informed action matches it, the
        stored entry did nothing this round and its quiet count goes up. That
        count is what prune() reads, so a store that never flips a decision
        eventually removes itself instead of being tuned forever.
        """
        outcome = self.memory.outcome(opportunity.slug)
        blind = self._evaluate(opportunity, None)
        if outcome is None:
            return blind
        informed = self._evaluate(opportunity, outcome)
        self.memory.note_decision(
            opportunity.slug, flipped=informed.action != blind.action
        )
        return informed

    def rank(self, opportunities: list[Opportunity]) -> list[Decision]:
        return sorted(
            (self.decide(item) for item in opportunities),
            key=lambda item: item.score,
            reverse=True,
        )
