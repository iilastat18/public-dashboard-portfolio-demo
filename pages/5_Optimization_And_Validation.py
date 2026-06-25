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
from src.mock_data import get_allocation_mix, get_optimizer_runs, get_validation_windows


st.set_page_config(page_title="Optimization And Validation", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="optimization_screenshot_mode",
    inactive_note="Navigate here first, then turn on Screenshot mode when you are ready to frame the frontier and validation panels.",
    active_note="Screenshot mode is on. The best crop here is usually the hero with the frontier and walk-forward panels.",
)

runs = get_optimizer_runs()
windows = get_validation_windows()
allocation = get_allocation_mix()

render_page_hero(
    "Optimization And Validation",
    "A synthetic scenario-analysis page inspired by optimizer-style workflows. It combines run scoring, recommended scenarios, walk-forward validation, and allocation mix views to make the product feel analytically serious.",
    kicker="Model-facing surface",
    pills=["scenario runs", "validation windows", "allocation mix"],
    side_label="Recommended runs",
    side_value=str(int((runs["status"] == "Recommended").sum())),
    side_copy="This is the kind of page that lets you talk about experimentation, model governance, and how results get communicated visually.",
)

render_filter_shell("Filters", "Compare optimizer outputs by bucket and scenario family.")
f1, f2, f3 = st.columns([0.9, 1.1, 1])
with f1:
    bucket = st.selectbox("Bucket", sorted(runs["bucket"].unique().tolist()), index=0)
with f2:
    scenario_filter = st.multiselect(
        "Scenario family",
        options=sorted(runs["scenario"].unique().tolist()),
        default=sorted(runs["scenario"].unique().tolist()),
    )
with f3:
    coverage_floor = st.slider("Coverage floor", min_value=90.0, max_value=99.0, value=94.5, step=0.1)

secondary_left, secondary_right = st.columns([1, 1.2])
with secondary_left:
    ranking_metric = st.segmented_control("Rank by", options=["score", "coverage", "expected_uplift", "stability"], default="score")
with secondary_right:
    color_mode = st.segmented_control("Color frontier by", options=["status", "scenario"], default="status")

filtered_runs = runs[(runs["bucket"] == bucket) & (runs["scenario"].isin(scenario_filter)) & (runs["coverage"] >= coverage_floor)]
filtered_windows = windows[windows["bucket"] == bucket]
filtered_alloc = allocation[allocation["bucket"] == bucket]
if filtered_runs.empty:
    st.warning("No optimizer runs match the current scenario filter. Re-enable one or more scenario families.")
    st.stop()

best_row = filtered_runs.sort_values(ranking_metric, ascending=False).iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Best scenario", best_row["scenario"])
col2.metric("Coverage", f"{best_row['coverage']:.2f}%")
col3.metric("Expected uplift", f"{best_row['expected_uplift']:.2f}")
col4.metric("Stability", f"{best_row['stability']:.2f}", f"risk {best_row['risk_score']:.2f}")

story_cols = st.columns(3)
for col, payload in zip(
    story_cols,
    [
        ("Evaluate", "The run table and scatter view show how you compare trade-offs instead of presenting one opaque output.", ["score", "trade-offs"]),
        ("Validate", "Walk-forward coverage gives you a cleaner story about robustness over time.", ["history", "robustness"]),
        ("Explain", "Allocation mix turns the result into something interpretable for a non-technical audience.", ["explanation", "weights"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

top_left, top_right = st.columns([1.05, 0.95])
with top_left:
    render_panel_title("Scenario frontier", "Coverage versus expected uplift, colored by scenario status.")
    frontier = (
        alt.Chart(filtered_runs)
        .mark_circle(size=220)
        .encode(
            x=alt.X("risk_score:Q", title="Risk score"),
            y=alt.Y("expected_uplift:Q", title="Expected uplift"),
            color=alt.Color(
                f"{color_mode}:N",
                scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]),
                title=color_mode.title(),
            ),
            size=alt.Size("coverage:Q", title="Coverage"),
            tooltip=["run_id:N", "scenario:N", "coverage:Q", "expected_uplift:Q", "risk_score:Q", "stability:Q", "status:N"],
        )
        .properties(height=330)
    )
    st.altair_chart(frontier, use_container_width=True)

with top_right:
    render_panel_title("Allocation mix", "Representative weights for the selected bucket.")
    alloc_chart = (
        alt.Chart(filtered_alloc)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#1f7763")
        .encode(
            x=alt.X("lever:N", title="Lever"),
            y=alt.Y("weight:Q", title="Weight (%)"),
            tooltip=["lever:N", alt.Tooltip("weight:Q", format=".2f")],
        )
        .properties(height=330)
    )
    st.altair_chart(alloc_chart, use_container_width=True)

bottom_left, bottom_right = st.columns([1.05, 0.95])
with bottom_left:
    render_panel_title("Walk-forward validation", "Observed versus target coverage over rolling windows.")
    validation_chart = (
        alt.Chart(filtered_windows)
        .transform_fold(["observed_coverage", "target_coverage"], as_=["series", "value"])
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("window_end:T", title="Window end"),
            y=alt.Y("value:Q", title="Coverage"),
            color=alt.Color(
                "series:N",
                scale=alt.Scale(range=["#1f7763", "#395c7d"]),
                title="Series",
            ),
            tooltip=["window_end:T", "series:N", alt.Tooltip("value:Q", format=".2f")],
        )
        .properties(height=320)
    )
    coverage_rule = alt.Chart(pd.DataFrame({"floor": [coverage_floor]})).mark_rule(color="#8b5322", strokeDash=[4, 4]).encode(y="floor:Q")
    st.altair_chart(validation_chart + coverage_rule, use_container_width=True)

with bottom_right:
    render_panel_title("Run table", "Sortable optimizer runs for the selected bucket.")
    selected_run_id = st.selectbox("Focus run", filtered_runs.sort_values(ranking_metric, ascending=False)["run_id"].tolist())
    selected_run = filtered_runs[filtered_runs["run_id"] == selected_run_id].iloc[0]
    render_surface_card(
        "Focused run detail",
        f"{selected_run['scenario']} in {selected_run['bucket']} scored {selected_run['score']:.2f} with {selected_run['coverage']:.2f}% coverage and {selected_run['rebalance_count']} rebalances.",
        chips=[selected_run["status"], f"risk {selected_run['risk_score']:.2f}", f"stability {selected_run['stability']:.2f}"],
    )
    display = filtered_runs.sort_values([ranking_metric, "coverage"], ascending=[False, False]).loc[
        :,
        ["run_id", "scenario", "coverage", "expected_uplift", "risk_score", "stability", "score", "status", "rebalance_count"],
    ]
    st.dataframe(display, use_container_width=True, hide_index=True)
