# Agentic Opportunity Engine

A persistent decision agent that ranks grants, hackathons and investment programs for a builder, remembers every application outcome, and changes future actions instead of starting from zero.

## Why it exists

Builders lose time to duplicate applications, expired programs and opportunities that do not match their real skills. A stateless ranking script repeats those mistakes every run. This agent uses durable application history and builder preferences to decide whether to apply, review or skip.

## Where Sibyl Memory is load-bearing

Sibyl Memory stores the active builder profile and the single source of truth for every application outcome. On every decision the engine recalls both before scoring.

Delete the memory layer and the product materially fails: a fresh process can no longer know that an application was already submitted or that a previous rejection exposed a fit problem. The included test proves the required fresh-session moment: session one chooses `apply` and records the outcome; a new `MemoryClient` opens the same database and changes the decision to `skip`.

## Run

```bash
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"
.venv/Scripts/opportunity-engine --db demo.db seed
.venv/Scripts/opportunity-engine --db demo.db rank
.venv/Scripts/opportunity-engine --db demo.db outcome sibyl-2026 applied
.venv/Scripts/opportunity-engine --db demo.db rank
.venv/Scripts/pytest -q
```

The second ranking changes because Sibyl recalls the persisted application outcome.

## Architecture

1. Opportunity sources provide verified program facts.
2. Sibyl Memory recalls builder preferences and prior outcomes.
3. The decision engine produces a scored `apply`, `review` or `skip` action.
4. Human approval remains required before any external application submission.
5. The outcome is written back so the next session starts smarter.

## Partner stacks

- **Sibyl Memory:** official Python client, on the critical decision path.
- **Base:** planned for verifiable payout and onchain project evidence; not claimed as completed until the transaction flow is visible in the demo.

## How memory made this possible

The useful output is not a list of links. It is a decision that compounds: no duplicate applications, remembered failure reasons and a queue adapted to the builder. Durable recall is what turns a one-off scraper into an agent that can be trusted to keep working.

## Prior Work declaration

This project reuses the author's earlier opportunity-discovery, SQLite queue, Telegram approval and MCP experiments as prior work. The Sibyl-backed decision memory, fresh-session behavior and this repository are hackathon work begun during the Sep 1-10, 2026 build window. Existing NFT and Base projects are evidence of domain experience, not presented as new hackathon code.

## Submission checklist

- [x] MIT license
- [x] Load-bearing Sibyl Memory integration
- [x] Fresh-session behavior test
- [x] Public GitHub repository
- [ ] Live opportunity-source adapter
- [ ] Base integration shown in product and demo
- [ ] Two-to-five minute demo video
- [ ] Public demo post and build-log post
