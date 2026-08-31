from __future__ import annotations

import argparse
from pathlib import Path

from .engine import OpportunityEngine
from .memory import OpportunityMemory
from .models import Opportunity


DEMO_OPPORTUNITIES = [
    Opportunity("sibyl-2026", "Sibyl Labs Hackathon", 10000, ("ai", "base"), ("python",)),
    Opportunity("telegraph-2026", "Telegraph Application Track", 1000, ("ai", "base"), ("python",)),
    Opportunity("generic-design", "Generic Design Contest", 500, ("design",), ("figma",)),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Memory-driven opportunity ranking agent")
    parser.add_argument("--db", default="opportunity_memory.db")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed", help="Store the builder profile in Sibyl Memory")
    sub.add_parser("rank", help="Rank sample opportunities using recalled memory")
    outcome = sub.add_parser("outcome", help="Persist an application outcome")
    outcome.add_argument("slug")
    outcome.add_argument("status", choices=["applied", "submitted", "rejected", "won"])
    outcome.add_argument("--reason", default="")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    memory = OpportunityMemory(Path(args.db))
    if args.command == "seed":
        memory.remember_profile(
            skills=["python", "mcp", "automation", "web3"],
            preferred_tags=["ai", "base", "agents", "web3"],
        )
        print("Builder profile persisted in Sibyl Memory.")
    elif args.command == "outcome":
        memory.remember_outcome(args.slug, args.status, args.reason)
        print(f"Outcome persisted: {args.slug} -> {args.status}")
    else:
        for decision in OpportunityEngine(memory).rank(DEMO_OPPORTUNITIES):
            reason = "; ".join(decision.reasons) or "reward/fit baseline"
            print(f"{decision.score:>3}  {decision.action:<6}  {decision.name} | {reason}")


if __name__ == "__main__":
    main()
