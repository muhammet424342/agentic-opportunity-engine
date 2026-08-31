# Demo script (2-3 minutes)

## 0:00-0:25 — Problem

"Builders waste hours rediscovering the same grants and forget why an opportunity was rejected or already submitted. Stateless scrapers produce links; they do not improve decisions."

Show the three demo opportunities and the empty/fresh database.

## 0:25-1:05 — First session

Run:

```powershell
.\.venv\Scripts\opportunity-engine.exe --db demo-video.db seed
.\.venv\Scripts\opportunity-engine.exe --db demo-video.db rank
```

Point out that Sibyl ranks the hackathon as `apply`, based on recalled builder skills and preferred stack.

## 1:05-1:30 — Persist an outcome

Run:

```powershell
.\.venv\Scripts\opportunity-engine.exe --db demo-video.db outcome sibyl-2026 submitted
```

Explain that the application outcome is stored through the official Sibyl Memory client, not process memory or a JSON mock.

## 1:30-2:10 — Genuine fresh-session recall

Close the terminal. Open a new terminal and run only:

```powershell
.\.venv\Scripts\opportunity-engine.exe --db demo-video.db rank
```

The Sibyl opportunity changes from `apply` to `skip`, with `Sibyl recalled prior status: submitted`. The core result changes because persisted context was recalled in a genuinely new process.

## 2:10-2:35 — Load-bearing proof

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Show the fresh-client test. Explain: remove Sibyl and the agent loses its builder profile, duplicates applications and cannot learn from rejection reasons.

## 2:35-2:55 — Product direction

Show the human-approval boundary and describe the next adapters: official opportunity sources, Base-verifiable project evidence and Telegram approval. Do not claim these as shipped until they are visible.
