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
from src.mock_data import get_performance_timeseries


st.set_page_config(page_title="Performance Monitoring", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="performance_screenshot_mode",
    inactive_note="Navigate here normally, then turn on Screenshot mode when you want a clean product shot.",
    active_note="Screenshot mode is on. This page is best captured from the hero through the trend and leaderboard sections.",
)

df = get_performance_timeseries()

render_page_hero(
    "Performance Monitoring",
    "A synthetic KPI surface for daily health, throughput, and queue pressure. The structure mirrors the kind of internal monitoring page that lets users scan, compare, and drill into segments quickly.",
    kicker="Core monitoring",
    pills=["KPI cards", "trend analysis", "segment comparison"],
    side_label="Latest date",
    side_value=str(df["date"].max().date()),
    side_copy="Use the controls below to change the operating window and focus on a specific team slice.",
)

render_filter_shell("Controls", "Switch between teams and operating windows without leaving the same surface.")
control_left, control_mid, control_right = st.columns([1, 1.1, 1.2])
with control_left:
    team_options = ["All"] + sorted(df["team"].unique().tolist())
    selected_team = st.selectbox("Team", team_options, index=0)
with control_mid:
    focus_label = st.segmented_control(
        "Focus metric",
        options=["Health score", "Throughput", "Accuracy", "Queue hours"],
        default="Health score",
    )
with control_right:
    lookback = st.slider("Lookback days", min_value=14, max_value=90, value=45, step=7)

metric_map = {
    "Health score": ("health_score", 90.0),
    "Throughput": ("throughput", 100.0),
    "Accuracy": ("accuracy", 95.0),
    "Queue hours": ("queue_hours", 24.0),
}
focus_metric, default_benchmark = metric_map[focus_label]
secondary_left, secondary_right = st.columns([1.15, 1])
with secondary_left:
    show_rolling = st.toggle("Show 7-day rolling average", value=True)
with secondary_right:
    benchmark = st.slider(
        "Benchmark target",
        min_value=float(default_benchmark * 0.7),
        max_value=float(default_benchmark * 1.25),
        value=float(default_benchmark),
        step=0.5,
    )

filtered = df[df["date"] >= df["date"].max() - pd.Timedelta(days=lookback - 1)]
if selected_team != "All":
    filtered = filtered[filtered["team"] == selected_team]
if filtered.empty:
    st.warning("No performance rows match the current filters. Try widening the lookback or selecting all teams.")
    st.stop()

latest = filtered[filtered["date"] == filtered["date"].max()]
prev = filtered[filtered["date"] == filtered["date"].max() - pd.Timedelta(days=7)]
if prev.empty:
    prev = latest

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg throughput", f"{latest['throughput'].mean():.1f}", f"{latest['throughput'].mean() - prev['throughput'].mean():+.1f} vs prior week")
col2.metric("Avg accuracy", f"{latest['accuracy'].mean():.2f}", f"{latest['accuracy'].mean() - prev['accuracy'].mean():+.2f}")
col3.metric("Queue hours", f"{latest['queue_hours'].mean():.1f}", f"{latest['queue_hours'].mean() - prev['queue_hours'].mean():+.1f}")
col4.metric("Health score", f"{latest['health_score'].mean():.1f}", f"{latest['health_score'].mean() - prev['health_score'].mean():+.1f}")

story_cols = st.columns(3)
story_cards = [
    (
        "Scan",
        "The first row is about speed: what changed today, which team is softening, and where queue pressure is building.",
        ["headline KPIs", "daily lens"],
    ),
    (
        "Compare",
        "The middle of the page helps compare teams and metrics across the selected operating window.",
        ["segments", "cross-team view"],
    ),
    (
        "Explain",
        "The snapshot table makes the latest numbers tangible and gives you a compact talking point for a walkthrough.",
        ["decision support", "summary table"],
    ),
]
for col, (title, body, chips) in zip(story_cols, story_cards):
    with col:
        render_surface_card(title, body, chips=chips)

render_panel_title(
    "Trend analysis",
    "Three synthetic signals tracked together to mimic a real monitoring surface with enough context for decisions.",
)

trend_view = filtered.copy()
if show_rolling:
    for column in ["throughput", "accuracy", "health_score", "queue_hours"]:
        trend_view[column] = trend_view.groupby("team")[column].transform(lambda s: s.rolling(7, min_periods=1).mean())

trend_df = trend_view.melt(
    id_vars=["date", "team"],
    value_vars=["throughput", "accuracy", "health_score", "queue_hours"],
    var_name="metric",
    value_name="value",
)
trend_df = trend_df[trend_df["metric"] == focus_metric]
benchmark_df = pd.DataFrame({"benchmark": [benchmark]})

chart = (
    alt.Chart(trend_df)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("value:Q", title=focus_label),
        color=alt.Color(
            "team:N",
            scale=alt.Scale(range=["#1f7763", "#d98d48", "#395c7d", "#8c6db1"]),
            title="Team",
        ),
        tooltip=["date:T", "team:N", alt.Tooltip("value:Q", format=".2f")],
    )
    .properties(height=360)
)
benchmark_rule = alt.Chart(benchmark_df).mark_rule(strokeDash=[4, 4], color="#8b5322", strokeWidth=2).encode(y="benchmark:Q")
st.altair_chart(chart + benchmark_rule, use_container_width=True)

left, right = st.columns([1.12, 1])
with left:
    render_panel_title("Metric leaderboard", "Teams ranked by the selected focus metric across the current window.")
    rank_df = (
        filtered.groupby("team", as_index=False)[[focus_metric]]
        .mean()
        .rename(columns={focus_metric: "value"})
        .sort_values("value", ascending=focus_metric == "queue_hours")
    )
    rank_df["rank"] = range(1, len(rank_df) + 1)
    compare_df = (
        rank_df
    )
    team_chart = (
        alt.Chart(compare_df)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("team:N", title="Team"),
            y=alt.Y("value:Q", title=focus_label),
            color=alt.Color("team:N", scale=alt.Scale(range=["#1f7763", "#d98d48", "#395c7d", "#8c6db1"]), title="Team"),
            tooltip=["team:N", alt.Tooltip("value:Q", format=".2f"), "rank:Q"],
        )
        .properties(height=280)
    )
    st.altair_chart(team_chart, use_container_width=True)

with right:
    render_panel_title("Latest operating snapshot", "Representative table for a compact decision review.")
    latest_table = latest.loc[:, ["team", "throughput", "accuracy", "queue_hours", "health_score"]].sort_values(
        "health_score", ascending=False
    )
    st.dataframe(latest_table, use_container_width=True, hide_index=True)
    leader = rank_df.iloc[0]
    render_surface_card(
        "Current leader",
        f"{leader['team']} is leading on {focus_label.lower()} for the selected window, which gives you a concrete talking point during a walkthrough.",
        chips=[f"rank #{int(leader['rank'])}", f"{leader['value']:.2f}"],
    )
