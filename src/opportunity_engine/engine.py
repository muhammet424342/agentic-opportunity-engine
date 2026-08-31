from __future__ import annotations

from .memory import OpportunityMemory
from .models import Decision, Opportunity


class OpportunityEngine:
    def __init__(self, memory: OpportunityMemory):
        self.memory = memory

    def decide(self, opportunity: Opportunity) -> Decision:
        profile = self.memory.profile()
        outcome = self.memory.outcome(opportunity.slug)
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

    def rank(self, opportunities: list[Opportunity]) -> list[Decision]:
        return sorted(
            (self.decide(item) for item in opportunities),
            key=lambda item: item.score,
            reverse=True,
        )
