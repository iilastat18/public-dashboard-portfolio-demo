<div align="center">
  <h1>Public Dashboard Portfolio Demo</h1>
  <p><strong>A privacy-safe multi-module analytics dashboard rebuilt with synthetic data and portfolio-safe product framing.</strong></p>
  <p>Designed to showcase dashboard architecture, metric storytelling, workflow support, and internal-tool product thinking.</p>
</div>

<p align="center">
  <code>dashboard design</code>
  <code>operations analytics</code>
  <code>synthetic data</code>
  <code>streamlit app</code>
  <code>product thinking</code>
</p>

## Portfolio Role

This is the broadest product demo in the portfolio. It shows how complex operational questions can be turned into a clean dashboard structure without exposing internal company material.

## Preview

![Analytics and operations dashboard demo](assets/dashboard-home.png)

## Positioning

This project can be described as a multi-module analytics and operations dashboard demo. It highlights how complex business questions can be translated into a clear interface with metrics, filters, investigation views, workflow helpers, and validation tooling.

## Suggested public scope

- Performance monitoring dashboard
- Exception review and anomaly tracking
- Data quality and validation views
- Optimization and scenario analysis
- Import and export utilities
- Operations playbook or workflow support page

## Skills this demo showcases

- Dashboard information architecture
- KPI design and metric storytelling
- Interactive filtering and drill-down analysis
- Data processing and validation workflows
- Multi-page app structure
- Streamlit-based internal tooling design
- Plotly and table-based reporting patterns

## Privacy note

This public version should be independently rebuilt. Do not copy internal code, screenshots, data files, field names, or workflow text directly from the company project. Use synthetic or public data and rename all business-specific concepts into generic portfolio-safe language.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Included starter files

- `app.py`: multipage Streamlit landing page with overview, snapshot tables, and navigation links
- `pages/0_Portfolio_Cover.py`: screenshot-friendly cover page for README or portfolio hero images
- `pages/1_Performance_Monitoring.py`: KPI monitoring and trend analysis
- `pages/2_Exception_Review.py`: anomaly review queue with severity and aging views
- `pages/3_Data_Quality.py`: validation health board and run history
- `pages/4_Operations_Workflow.py`: workflow board with SLA risk and handoff lanes
- `pages/5_Optimization_And_Validation.py`: scenario analysis, validation windows, and allocation mix
- `pages/6_Universe_Explorer.py`: searchable universe explorer with coverage and readiness views
- `src/demo_content.py`: public-safe product framing and module descriptions
- `src/mock_data.py`: deterministic synthetic datasets for the demo
- `src/dashboard_ui.py`: shared design system helpers and styling
- `docs/PRODUCT_STRUCTURE.md`: public-facing product structure map
- `docs/PORTFOLIO_COPY.md`: ready-to-use portfolio text
- `docs/SAFE_REBUILD_CHECKLIST.md`: pre-publish safety checklist

## Suggested repo name

- `analytics-ops-dashboard-demo`
- `interactive-analytics-dashboard`
- `portfolio-dashboard-demo`

## Suggested public module set

If you want to keep expanding the public demo, these are good portfolio-safe modules to build around:

- Performance Monitoring
- Exception Review
- Data Quality
- Operations Workflow
- Optimization And Validation
- Universe Explorer

## Suggested tech stack section

You can adapt this depending on what you want to show publicly:

- Python
- Streamlit
- Pandas or Polars
- Plotly
- DuckDB
- Synthetic CSV or Parquet datasets

## Ready-to-use short description

Built a privacy-safe multi-module analytics dashboard demo focused on KPI monitoring, anomaly investigation, data validation, and workflow support. The public version is independently rebuilt with synthetic data and generic business terminology.

## Screenshot Strategy

- lead with `pages/0_Portfolio_Cover.py` for the README hero image
- use one screenshot of the KPI / monitoring page
- use one screenshot of the validation or workflow page
- keep screenshots focused on layout, hierarchy, and product feel rather than dense tables only

## Next steps

1. Rebuild only the UI and logic patterns you personally want to showcase.
2. Replace all company-specific names, labels, and workflows.
3. Use mock or public datasets only.
4. Add screenshots from the rebuilt public version, not the internal one.

## Screenshot tip

Open `pages/0_Portfolio_Cover.py` in the running app when you want a clean screenshot for your GitHub README.
