# Submission copy

## One-line description

Agentic Opportunity Engine is a persistent grant and hackathon decision agent that remembers every application and changes what it recommends in future sessions.

## Short description

Opportunity discovery is not the hard part; remembering what happened and making a better next decision is. Agentic Opportunity Engine ranks programs against a builder's proven skills, recalls submitted or rejected applications through Sibyl Memory, and returns an actionable apply/review/skip queue. A fresh session materially changes its decision using the persisted record, preventing duplicate submissions and repeated fit mistakes.

## Sibyl Memory use

The official Sibyl Memory Python client stores the builder profile and application outcomes as the decision engine's source of truth. Every ranking recalls both. If the memory layer is removed, the engine loses its identity-specific fit signals and cannot know that a program was already submitted; its core promise fails.

## Build-log post draft

Building Agentic Opportunity Engine for @sibylcap: a grant and hackathon agent that does not restart from zero. Today the fresh-session test works—after an application outcome is persisted through Sibyl Memory, a new process recalls it and changes `apply` to `skip`. Next: live verified sources and Base evidence. #BuildInPublic

## Demo post draft

Agentic Opportunity Engine turns opportunity links into decisions that compound. In the demo, a fresh agent session recalls a prior submission from Sibyl Memory and changes its action, preventing a duplicate application. Built for the Sibyl Labs Hackathon with an explicit human approval boundary. @sibylcap
