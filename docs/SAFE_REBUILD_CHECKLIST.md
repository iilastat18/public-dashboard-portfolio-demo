# Safe Rebuild Checklist

Use this checklist before publishing anything to GitHub.

## Never publish directly

- Internal repository names
- Company name, team name, or client name
- Real screenshots from the internal dashboard
- Real CSV, Excel, Parquet, JSON, or cache files
- Internal field names, abbreviations, and status codes
- API keys, tokens, URLs, hostnames, or SSO configuration
- Internal workflow steps copied word-for-word
- Exact alert thresholds or optimization rules tied to the business

## Replace with generic versions

- Real business labels -> generic module names
- Real KPIs -> sample or synthetic KPIs
- Real entities -> mock instruments, products, or regions
- Real workflows -> simplified public demo flows
- Real data -> synthetic, sampled, or public datasets

## Good public framing

- "analytics dashboard demo"
- "operations tooling prototype"
- "KPI monitoring and anomaly review"
- "data quality and validation interface"
- "interactive reporting workflow"

## Final self-check

Ask yourself these questions:

1. If a coworker saw this repo, would they recognize the internal project immediately?
2. Does any file reveal how the company operates internally?
3. Does any dataset contain real business records, identifiers, or logic?
4. Did I write this version independently enough to stand on its own?

If any answer feels unsafe, remove or rewrite the content before publishing.
