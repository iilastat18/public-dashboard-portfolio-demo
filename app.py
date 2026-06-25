from __future__ import annotations

import altair as alt
import streamlit as st

from src.dashboard_ui import (
    apply_theme,
    enable_screenshot_mode,
    render_metric_strip,
    render_page_hero,
    render_panel_title,
    render_surface_card,
)
from src.demo_content import MODULE_GROUPS, PRIVACY_PRINCIPLES, SHORT_DESCRIPTION
from src.mock_data import (
    get_exception_cases,
    get_optimizer_runs,
    get_performance_timeseries,
    get_quality_checks,
    get_universe_records,
    get_workflow_items,
)


st.set_page_config(
    page_title="Analytics And Operations Dashboard Demo",
    page_icon=":bar_chart:",
    layout="wide",
)
apply_theme()
enable_screenshot_mode(
    toggle_key="home_screenshot_mode",
    inactive_note="Turn on Screenshot mode after you land on the page you want to capture.",
    active_note="Screenshot mode is on. Capture the main hero, metric strip, and whichever module section you want to feature.",
)

performance_df = get_performance_timeseries()
exception_df = get_exception_cases()
quality_df = get_quality_checks()
workflow_df = get_workflow_items()
optimizer_df = get_optimizer_runs()
universe_df = get_universe_records()

latest_day = performance_df["date"].max()
latest_perf = performance_df[performance_df["date"] == latest_day]
open_exceptions = int((exception_df["status"] != "Resolved").sum())
blocking_checks = int((quality_df["status"] == "Blocked").sum())
inflight_tasks = int((workflow_df["lane"] != "Published").sum())
recommended_runs = int((optimizer_df["status"] == "Recommended").sum())

render_page_hero(
    "Analytics And Operations Dashboard Demo",
    "A richer analytics dashboard demo that combines KPI tracking, review queues, validation surfaces, operational lanes, universe search, and optimization monitoring in one cohesive product shell.",
    kicker="Portfolio demo",
    pills=["Monitoring", "Exception Review", "Validation", "Workflow", "Universe Search", "Optimization"],
    side_label="Product scope",
    side_value="6 surfaces",
    side_copy="Built to show system thinking, reusable UI patterns, and independent reconstruction rather than a sanitized export of internal work.",
)

render_metric_strip(
    [
        {"label": "Composite health score", "value": f"{latest_perf['health_score'].mean():.1f}", "delta": "synthetic daily snapshot"},
        {"label": "Open exception cases", "value": f"{open_exceptions}", "delta": "active review queue"},
        {"label": "Blocking quality checks", "value": f"{blocking_checks}", "delta": "watchlist"},
        {"label": "In-flight tasks", "value": f"{inflight_tasks}", "delta": "workflow board"},
        {"label": "Recommended scenarios", "value": f"{recommended_runs}", "delta": "optimizer runs"},
    ]
)

upper_left, upper_right = st.columns([1.35, 1])

with upper_left:
    render_panel_title(
        "Why this feels closer to a real product",
        "The demo is organized as connected surfaces rather than a single landing page. Each module has its own point of view and dataset, but the information design stays consistent across the app.",
    )
    feature_cols = st.columns(3)
    feature_cards = [
        (
            "Analytical depth",
            "Trend lines, segment comparisons, scoring views, and validation windows add more than just decorative charts.",
            ["KPI logic", "comparisons", "explanations"],
        ),
        (
            "Operational realism",
            "Exception queues, SLA lanes, and quality checks make the product feel like a working internal tool, not a static report.",
            ["queues", "lanes", "audit views"],
        ),
        (
            "Portfolio safety",
            "All terms, scenarios, and datasets are synthetic and organized for portfolio presentation.",
            ["synthetic data", "mock data", "renamed modules"],
        ),
    ]
    for col, (title, body, chips) in zip(feature_cols, feature_cards):
        with col:
            render_surface_card(title, body, chips=chips)

    render_panel_title("Seven-day operating pulse", "A high-level read across throughput, accuracy, and composite health.")
    pulse_df = (
        performance_df.groupby("date", as_index=False)[["throughput", "accuracy", "health_score"]]
        .mean()
        .tail(7)
        .melt("date", var_name="metric", value_name="value")
    )
    pulse_chart = (
        alt.Chart(pulse_df)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("value:Q", title="Score"),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(range=["#1f7763", "#d98d48", "#395c7d"]),
                title="Metric",
            ),
            tooltip=["date:T", "metric:N", alt.Tooltip("value:Q", format=".2f")],
        )
        .properties(height=310)
    )
    st.altair_chart(pulse_chart, use_container_width=True)

with upper_right:
    render_panel_title(
        "Explore the demo",
        "Each page is designed as a standalone product surface you could point to in a portfolio walkthrough.",
    )
    nav_cols = st.columns(2)
    nav_targets = [
        ("Performance Monitoring", "pages/1_Performance_Monitoring.py"),
        ("Exception Review", "pages/2_Exception_Review.py"),
        ("Data Quality", "pages/3_Data_Quality.py"),
        ("Operations Workflow", "pages/4_Operations_Workflow.py"),
        ("Optimization And Validation", "pages/5_Optimization_And_Validation.py"),
        ("Universe Explorer", "pages/6_Universe_Explorer.py"),
    ]
    for index, (label, path) in enumerate(nav_targets):
        with nav_cols[index % 2]:
            st.page_link(path, label=label)

    render_panel_title("Public-safe positioning", SHORT_DESCRIPTION)
    for item in PRIVACY_PRINCIPLES:
        st.markdown(f"- {item}")

render_panel_title(
    "Module architecture",
    "The internal-style toolset has been regrouped into public-facing module families that still communicate product breadth.",
)
for group in MODULE_GROUPS:
    st.subheader(group["name"])
    cols = st.columns(len(group["modules"]))
    for col, module in zip(cols, group["modules"]):
        with col:
            render_surface_card(module["name"], module["description"], chips=module["signals"])

render_panel_title(
    "Live snapshots",
    "Quick previews from the synthetic datasets behind the product surfaces.",
)
tab_a, tab_b, tab_c, tab_d = st.tabs(["Exceptions", "Quality", "Workflow", "Universe"])

with tab_a:
    preview = (
        exception_df.sort_values(["severity_rank", "aging_hours"], ascending=[False, False])
        .loc[:, ["case_id", "category", "severity", "status", "owner", "aging_hours", "impact_score"]]
        .head(10)
    )
    st.dataframe(preview, use_container_width=True, hide_index=True)

with tab_b:
    preview = (
        quality_df.sort_values(["status_rank", "failed_checks"], ascending=[False, False])
        .loc[:, ["dataset", "status", "freshness_minutes", "missing_rate", "failed_checks"]]
    )
    st.dataframe(preview, use_container_width=True, hide_index=True)

with tab_c:
    preview = (
        workflow_df.sort_values(["lane_rank", "sla_hours_left"])
        .loc[:, ["task_id", "lane", "task_type", "owner", "sla_hours_left", "priority"]]
    )
    st.dataframe(preview, use_container_width=True, hide_index=True)

with tab_d:
    preview = (
        universe_df.sort_values(["readiness_score", "mapping_gaps"], ascending=[True, False])
        .loc[:, ["instrument_id", "display_name", "asset_class", "region", "coverage_status", "readiness_score", "mapping_gaps"]]
        .head(12)
    )
    st.dataframe(preview, use_container_width=True, hide_index=True)
