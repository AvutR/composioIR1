# Composio App Research Agent

Resumable pipeline for researching 100 apps across 10 categories. This scaffold deliberately does not invent an app list or evidence: replace `config/apps.csv` with the approved 100-row list.

## Run order
1. `python scripts/fetch.py` — candidate discovery, concurrent Composio search/fetch, raw cache.
2. Configure `llm_json()` and run `python scripts/extract.py` — batches of 9, resumable per app.
3. `python scripts/verify.py` — grounding checks and spot-check ledger. Add critic batching in the same adapter for flagged rows.
4. `python scripts/reduce.py` — deterministic aggregates and fixture test.
5. Run one synthesis prompt using only `data/aggregates.json`; verify every cited number.
6. Render `output/report.html` with headline patterns, matrix, workflow, verification, and repo link.

## Composio integration
`fetch.py` is the integration seam: map `composio_search` to `COMPOSIO_SEARCH_WEB` and `composio_fetch` to `COMPOSIO_SEARCH_FETCH_URL_CONTENT` in the playground/worker adapter. Do not substitute unaudited direct HTTP for the required Composio search/fetch path. The LLM adapter must support structured JSON and batch calls.

## Evidence and limitations
Every populated field must have a URL-backed evidence item from fetched text. Scripted grounding is a keyword screen, not proof. Human checks are required; populate `data/spot_checks.json` honestly. Pages blocked by robots, login, JavaScript rendering, or partner gates may produce `blocked` or `none_found`; never infer access from absence.

## Target structure
`data/raw/` cache · `data/extracted/` per-app outputs · `scripts/` stages · `output/report.html`.
