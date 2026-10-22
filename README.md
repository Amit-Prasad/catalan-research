# Catalan

A research programme about intelligent search: *here is a space of possibilities, learn what is worth exploring.*

This repository is the programme's site. It holds the hub and the research logs.

| Path | What it is |
|---|---|
| `index.html` | The hub: the six open questions, and an index of what has come back from them |
| `search-trees/` | Log 1 — a tree search over six thousand LLM-written trading strategies, and what it taught us about LLM-driven search |
| `search-trees/trees/` | Twenty tree snapshots the log's explorer reads, plus a manifest describing them |

## Log 1 — the search trees

Sixteen language models wrote intraday trading strategies for the Nifty 50 between June and September 2026, inside a Monte Carlo tree search that decided where each backtest went. The search produced a leaderboard. The leaderboard is void, and why it is void is the result: nine failures in the scoring and validation rules, two of which void it outright.

Every score in the log and in the explorer is an **evaluation score** — the number the search ranked on, computed on windows drawn from the same history the search was free to fit. None of them is a return, and none was measured on data the search had never seen. The rebuilt validation is reported as dated updates as its results land.

The snapshots carry each node's id, parent, visit count, scores, the model that wrote it, its idea in one line, and its six backtest metrics. They do not carry the strategy source.

## The engine

The search itself is [Pathfinder](https://github.com/Amit-Prasad/pathfinder), a Monte Carlo tree search over programs. The market application that Log 1 reports on is a separate, private project.

## Prior work

ERA, Aygün et al., [arXiv:2509.06503](https://arxiv.org/abs/2509.06503).

## Serving it

Static files, no build step. The log fetches its snapshots over HTTP, so it needs a server rather than being opened from disk:

```sh
python3 -m http.server 8000     # then open http://localhost:8000
```
