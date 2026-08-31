from opportunity_engine.engine import OpportunityEngine
from opportunity_engine.memory import OpportunityMemory
from opportunity_engine.models import Opportunity


def test_fresh_session_recall_changes_decision(tmp_path):
    db = tmp_path / "sibyl.db"
    opportunity = Opportunity(
        "sibyl-2026", "Sibyl Labs Hackathon", 10000, ("ai", "base"), ("python",)
    )

    first_session = OpportunityMemory(db)
    first_session.remember_profile(
        skills=["python", "automation"], preferred_tags=["ai", "base"]
    )
    before = OpportunityEngine(first_session).decide(opportunity)
    assert before.action == "apply"
    first_session.remember_outcome("sibyl-2026", "applied")

    # A genuinely new client opens the same Sibyl DB in a fresh session.
    fresh_session = OpportunityMemory(db)
    after = OpportunityEngine(fresh_session).decide(opportunity)
    assert after.action == "skip"
    assert after.score == 0
    assert "Sibyl recalled prior status" in after.reasons[0]
