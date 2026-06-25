from __future__ import annotations

import altair as alt
import streamlit as st

from src.dashboard_ui import apply_theme, enable_screenshot_mode, render_metric_strip, render_page_hero, render_panel_title, render_surface_card
from src.mock_data import (
    get_exception_cases,
    get_optimizer_runs,
    get_performance_timeseries,
    get_quality_checks,
    get_universe_records,
)


st.set_page_config(
    page_title="Portfolio Cover",
    page_icon=":sparkles:",
    layout="wide",
)
apply_theme()
enable_screenshot_mode(
    toggle_key="cover_screenshot_mode",
    inactive_note="Turn on Screenshot mode only when you want to capture a clean README cover.",
    active_note="README cover mode is on. Capture the hero plus first two rows.",
)

perf = get_performance_timeseries()
exc = get_exception_cases()
quality = get_quality_checks()
optimizer = get_optimizer_runs()
universe = get_universe_records()

latest_perf = perf[perf["date"] == perf["date"].max()]
open_cases = int((exc["status"] != "Resolved").sum())
recommended = int((optimizer["status"] == "Recommended").sum())
missing_coverage = int((universe["coverage_status"] == "Missing").sum())

render_page_hero(
    "Analytics Dashboard Portfolio",
    "A polished product demo that combines monitoring, anomaly review, validation, workflow tooling, search, and optimization into one portfolio-ready analytics surface.",
    kicker="README cover",
    pills=["Portfolio-safe", "Synthetic data", "Multi-module", "Interview-ready"],
    side_label="Best use",
    side_value="GitHub hero",
    side_copy="Designed specifically as a screenshot-friendly landing page so you can show product depth before anyone reads the repository.",
)

render_metric_strip(
    [
        {"label": "Health score", "value": f"{latest_perf['health_score'].mean():.1f}", "delta": "daily synthetic pulse"},
        {"label": "Open reviews", "value": f"{open_cases}", "delta": "exception queue"},
        {"label": "Recommended scenarios", "value": f"{recommended}", "delta": "optimization layer"},
        {"label": "Coverage gaps", "value": f"{missing_coverage}", "delta": "universe explorer"},
        {"label": "Module surfaces", "value": "6", "delta": "plus screenshot cover"},
    ]
)

top_left, top_right = st.columns([1.18, 0.82])
with top_left:
    render_panel_title("Product snapshot", "A cover-friendly view of how the demo balances monitoring, search, validation, and scenario analysis.")
    pulse = (
        perf.groupby("date", as_index=False)[["throughput", "accuracy", "health_score"]]
        .mean()
        .tail(14)
        .melt("date", var_name="metric", value_name="value")
    )
    pulse_chart = (
        alt.Chart(pulse)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("value:Q", title="Score"),
            color=alt.Color("metric:N", scale=alt.Scale(range=["#1f7763", "#d98d48", "#395c7d"]), title=None),
            tooltip=["date:T", "metric:N", alt.Tooltip("value:Q", format=".2f")],
        )
        .properties(height=320)
    )
    st.altair_chart(pulse_chart, use_container_width=True)

with top_right:
    card_cols = st.columns(2)
    card_specs = [
        ("Monitoring", "Trend lines, benchmark views, and leaderboard logic make the top layer feel like a real operating dashboard.", ["KPI", "trend", "leaderboard"]),
        ("Review", "Exception queues, owner aging, and focused case detail add operational credibility.", ["triage", "owner", "SLA"]),
        ("Validation", "Freshness and failure thresholds turn data quality into a dashboard surface, not just a table.", ["checks", "thresholds", "history"]),
        ("Optimization", "Scenario runs and walk-forward coverage make the product feel analytically mature.", ["frontier", "validation", "allocation"]),
    ]
    for col, spec in zip(card_cols * 2, card_specs):
        with col:
            render_surface_card(spec[0], spec[1], chips=spec[2])

middle_left, middle_right = st.columns([0.9, 1.1])
with middle_left:
    render_panel_title("Coverage posture", "A compact summary from the explorer module.")
    coverage = universe.groupby(["coverage_status"], as_index=False).size()
    coverage_chart = (
        alt.Chart(coverage)
        .mark_arc(innerRadius=54, outerRadius=112)
        .encode(
            theta=alt.Theta("size:Q"),
            color=alt.Color("coverage_status:N", scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]), title=None),
            tooltip=["coverage_status:N", "size:Q"],
        )
        .properties(height=280)
    )
    st.altair_chart(coverage_chart, use_container_width=True)

with middle_right:
    render_panel_title("Scenario score frontier", "A screenshot-friendly preview of the optimization page.")
    frontier = (
        alt.Chart(optimizer)
        .mark_circle(size=170)
        .encode(
            x=alt.X("risk_score:Q", title="Risk"),
            y=alt.Y("expected_uplift:Q", title="Uplift"),
            color=alt.Color("status:N", scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]), title=None),
            size=alt.Size("coverage:Q", title=None),
            tooltip=["run_id:N", "scenario:N", "coverage:Q", "expected_uplift:Q", "risk_score:Q", "status:N"],
        )
        .properties(height=280)
    )
    st.altair_chart(frontier, use_container_width=True)

bottom_cols = st.columns(3)
for col, payload in zip(
    bottom_cols,
    [
        ("Synthetic demo", "Everything here is synthetic and organized to highlight product structure, dashboard design, and workflow-oriented analytics.", ["synthetic data", "portfolio demo"]),
        ("Good for screenshots", "This page is intentionally composed so the hero, charts, and cards fit neatly into a GitHub README image crop.", ["hero-ready", "balanced layout"]),
        ("Good for interviews", "You can walk someone from this cover page into monitoring, review, validation, optimization, and search without changing the story.", ["demo flow", "talk track"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

st.page_link("app.py", label="Open dashboard home")
