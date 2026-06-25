from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from src.dashboard_ui import (
    apply_theme,
    enable_screenshot_mode,
    render_filter_shell,
    render_page_hero,
    render_panel_title,
    render_surface_card,
)
from src.mock_data import get_quality_checks, get_quality_run_history


st.set_page_config(page_title="Data Quality", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="quality_screenshot_mode",
    inactive_note="Open the page you want first, then switch on Screenshot mode right before capturing.",
    active_note="Screenshot mode is on. This page usually looks best with the hero and Health Board tab in frame.",
)

checks = get_quality_checks().copy()
history = get_quality_run_history()

render_page_hero(
    "Data Quality",
    "A synthetic validation control panel that shows health checks, freshness drift, and run history. This page is meant to demonstrate how you design a data-facing operational dashboard rather than just a reporting page.",
    kicker="Validation surface",
    pills=["health board", "freshness checks", "run history"],
    side_label="Datasets tracked",
    side_value=str(len(checks)),
    side_copy="The visuals are synthetic, but the interaction pattern mirrors what a quality dashboard needs: status, freshness, and failure context.",
)

render_filter_shell("Filters", "Limit the page to specific owners or quality states.")
filter_left, filter_mid, filter_right = st.columns([1, 1, 1.05])
with filter_left:
    owner_filter = st.multiselect(
        "Owner",
        options=sorted(checks["owner"].unique().tolist()),
        default=sorted(checks["owner"].unique().tolist()),
    )
with filter_mid:
    status_filter = st.multiselect(
        "Status",
        options=["Healthy", "Watch", "Blocked"],
        default=["Healthy", "Watch", "Blocked"],
    )
with filter_right:
    freshness_limit = st.slider("Freshness threshold", min_value=20, max_value=120, value=60, step=5)

secondary_left, secondary_right = st.columns([1, 1.1])
with secondary_left:
    missing_limit = st.slider("Missing-rate threshold", min_value=0.2, max_value=3.0, value=1.4, step=0.1)
with secondary_right:
    breach_only = st.toggle("Only show threshold breaches", value=False)

filtered = checks[checks["owner"].isin(owner_filter) & checks["status"].isin(status_filter)]
if breach_only:
    filtered = filtered[
        (filtered["freshness_minutes"] >= freshness_limit)
        | (filtered["missing_rate"] >= missing_limit)
        | (filtered["failed_checks"] >= 2)
    ]
if filtered.empty:
    st.warning("No datasets match the current filters. Try re-enabling more owners or statuses.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Datasets checked", f"{len(filtered)}")
col2.metric("Freshness avg", f"{filtered['freshness_minutes'].mean():.0f} min")
col3.metric("Failed checks", f"{filtered['failed_checks'].sum():.0f}")
col4.metric("Blocked datasets", f"{(filtered['status'] == 'Blocked').sum()}")

story_cols = st.columns(3)
for col, payload in zip(
    story_cols,
    [
        ("Health", "The scatter view gives the user a quick sense of which datasets are both stale and fragile.", ["status", "freshness"]),
        ("Audit", "The table grounds the page in concrete checks rather than abstract dashboard polish.", ["failures", "schema change"]),
        ("Validation rhythm", "Run history turns the page into a system-health story over time, which is useful in portfolio demos.", ["trend", "ops cadence"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

tab1, tab2 = st.tabs(["Health Board", "Run History"])

with tab1:
    left, right = st.columns([1.15, 1])
    with left:
        render_panel_title("Dataset status board", "A validation control panel for freshness, failures, and review status.")
        status_chart = (
            alt.Chart(filtered)
            .mark_circle(size=240)
            .encode(
                x=alt.X("freshness_minutes:Q", title="Freshness (minutes)"),
                y=alt.Y("missing_rate:Q", title="Missing rate"),
                color=alt.Color(
                    "status:N",
                    scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]),
                    title="Status",
                ),
                size=alt.Size("failed_checks:Q", title="Failed checks"),
                tooltip=["dataset:N", "owner:N", "status:N", "freshness_minutes:Q", "missing_rate:Q", "failed_checks:Q"],
            )
            .properties(height=340)
        )
        freshness_rule = alt.Chart(pd.DataFrame({"x": [freshness_limit]})).mark_rule(color="#8b5322", strokeDash=[4, 4]).encode(x="x:Q")
        missing_rule = alt.Chart(pd.DataFrame({"y": [missing_limit]})).mark_rule(color="#8b5322", strokeDash=[4, 4]).encode(y="y:Q")
        st.altair_chart(status_chart + freshness_rule + missing_rule, use_container_width=True)
    with right:
        render_panel_title("Current check table", "Compact audit view for freshness, failures, and schema changes.")
        display = filtered.sort_values(["status_rank", "failed_checks"], ascending=[False, False]).loc[
            :,
            ["dataset", "owner", "status", "freshness_minutes", "missing_rate", "failed_checks", "schema_changes"],
        ]
        st.dataframe(display, use_container_width=True, hide_index=True)
        selected_dataset = st.selectbox("Inspect dataset", display["dataset"].tolist())
        dataset_row = filtered[filtered["dataset"] == selected_dataset].iloc[0]
        render_surface_card(
            "Dataset detail",
            f"{selected_dataset} is owned by {dataset_row['owner']} with {dataset_row['row_count']:,} synthetic rows and {dataset_row['schema_changes']} schema changes tracked.",
            chips=[dataset_row["status"], f"{dataset_row['failed_checks']} failed checks", f"{dataset_row['freshness_minutes']} min fresh"],
        )

with tab2:
    render_panel_title("Validation run history", "Trend view for pipeline quality over time.")
    trend = history.melt("run_date", var_name="metric", value_name="count")
    history_chart = (
        alt.Chart(trend)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("run_date:T", title="Run date"),
            y=alt.Y("count:Q", title="Check count"),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(range=["#1f7763", "#d98d48", "#395c7d"]),
                title="Metric",
            ),
            tooltip=["run_date:T", "metric:N", "count:Q"],
        )
        .properties(height=340)
    )
    st.altair_chart(history_chart, use_container_width=True)
