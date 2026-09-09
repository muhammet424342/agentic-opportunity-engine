from opportunity_engine.engine import OpportunityEngine
from opportunity_engine.memory import TOMBSTONE, OpportunityMemory
from opportunity_engine.models import Opportunity


SIBYL = Opportunity("sibyl-2026", "Sibyl Labs Hackathon", 10000, ("ai", "base"), ("python",))
DESIGN = Opportunity("generic-design", "Generic Design Contest", 500, ("design",), ("figma",))


def _seeded(db):
    memory = OpportunityMemory(db)
    memory.remember_profile(skills=["python", "automation"], preferred_tags=["ai", "base"])
    return memory


def test_flipping_entry_never_goes_quiet(tmp_path):
    memory = _seeded(tmp_path / "sibyl.db")
    memory.remember_outcome(SIBYL.slug, "applied")
    engine = OpportunityEngine(memory)

    for _ in range(5):
        assert engine.decide(SIBYL).action == "skip"

    # It flips apply -> skip every single time, so the clock keeps resetting.
    assert memory.trail(SIBYL.slug)["quiet_decisions"] == 0
    assert memory.prune(3) == []


def test_quiet_entry_is_tombstoned_and_keeps_its_reason(tmp_path):
    memory = _seeded(tmp_path / "sibyl.db")
    # "rejected" only shaves 25 points off an already-low score, so the action
    # is skip either way: the entry is on file but changes nothing.
    memory.remember_outcome(DESIGN.slug, "rejected", reason="wrong stack")
    engine = OpportunityEngine(memory)

    blind_action = engine._evaluate(DESIGN, None).action
    for _ in range(3):
        assert engine.decide(DESIGN).action == blind_action
    assert memory.trail(DESIGN.slug)["quiet_decisions"] == 3

    assert memory.prune(3) == [DESIGN.slug]

    record = memory.trail(DESIGN.slug)
    assert record["status"] == TOMBSTONE
    assert record["reason"] == "wrong stack"  # the trail survives the payload
    assert record["was"] == "rejected"
    assert record["pruned_after"] == 3

    # Payload is gone, so the decision layer can no longer see it at all.
    assert memory.outcome(DESIGN.slug) is None
    assert engine.decide(DESIGN).action == blind_action
    assert memory.prune(1) == []  # a tombstone is not pruned twice


def test_clock_counts_decisions_not_time(tmp_path):
    """An idle agent must not age its own memory out."""
    memory = _seeded(tmp_path / "sibyl.db")
    memory.remember_outcome(DESIGN.slug, "rejected", reason="wrong stack")

    # No decisions taken: no time has passed as far as the store is concerned.
    assert memory.trail(DESIGN.slug)["quiet_decisions"] == 0
    assert memory.prune(1) == []

    OpportunityEngine(memory).decide(DESIGN)
    assert memory.trail(DESIGN.slug)["quiet_decisions"] == 1
    assert memory.prune(1) == [DESIGN.slug]
