from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Opportunity:
    slug: str
    name: str
    reward_usd: int
    tags: tuple[str, ...] = field(default_factory=tuple)
    requirements: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Decision:
    slug: str
    name: str
    score: int
    action: str
    reasons: tuple[str, ...]
