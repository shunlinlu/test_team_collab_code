# test-team-collab

Practice project for exercising the team-collab workflow. Ships a minimal
data-acquisition (数采) demo.

## Data-acquisition demo

`collector/collect.py` periodically samples the host's load average and appends
each reading to a CSV. Standard library only (macOS/Linux).

```bash
# take 5 samples, 1s apart, into data/samples.csv
python3 collector/collect.py

# custom output / count / interval
python3 collector/collect.py --out data/run1.csv --count 10 --interval 0.5
```

Output columns: `timestamp, load1, load5, load15`.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Team-collab

Shared project state lives in `obsidian-docs/` (CURRENT / NEXT / RISKS / TODO).
See `AGENTS.md` for the agent workflow.
