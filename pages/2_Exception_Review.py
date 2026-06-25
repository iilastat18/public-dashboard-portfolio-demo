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
from src.mock_data import get_exception_cases


st.set_page_config(page_title="Exception Review", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="exception_screenshot_mode",
    inactive_note="Use the sidebar to reach this page first, then turn on Screenshot mode for a cleaner queue capture.",
    active_note="Screenshot mode is on. The strongest crop is usually the hero, status breakdown, and case-detail area.",
)

df = get_exception_cases().copy()

render_page_hero(
    "Exception Review",
    "A synthetic anomaly queue designed to feel closer to a real operational review tool. The page combines severity filters, ownership views, aging analysis, and a sortable case list in one place.",
    kicker="Review workflow",
    pills=["severity filter", "owner lens", "aging analysis"],
    side_label="Open queue",
    side_value=str(int((df["status"] != "Resolved").sum())),
    side_copy="Use this page to show how you think about investigation flow, escalation, and queue health.",
)

render_filter_shell("Filters", "Narrow the review queue by severity, status, and owner.")
f1, f2, f3, f4 = st.columns([1.05, 1.15, 0.9, 1])
with f1:
    severity_options = st.multiselect(
        "Severity",
        options=["Low", "Medium", "High", "Critical"],
        default=["Medium", "High", "Critical"],
    )
with f2:
    status_options = st.multiselect(
        "Status",
        options=sorted(df["status"].unique().tolist()),
        default=sorted(df["status"].unique().tolist()),
    )
with f3:
    owner_options = ["All"] + sorted(df["owner"].unique().tolist())
    owner = st.selectbox("Owner", owner_options, index=0)
with f4:
    aging_threshold = st.slider("Aging threshold (h)", min_value=12, max_value=168, value=72, step=12)

secondary_left, secondary_right = st.columns([1.2, 1])
with secondary_left:
    breakdown = st.segmented_control("Breakdown", options=["Severity", "Category", "Module"], default="Severity")
with secondary_right:
    sla_only = st.toggle("Only SLA-breached open cases", value=False)

filtered = df[df["severity"].isin(severity_options) & df["status"].isin(status_options)]
if owner != "All":
    filtered = filtered[filtered["owner"] == owner]
if sla_only:
    filtered = filtered[(filtered["status"] != "Resolved") & (filtered["aging_hours"] >= aging_threshold)]
if filtered.empty:
    st.warning("No cases match the current filters. Try widening severity, status, or owner selection.")
    st.stop()

resolved_ratio = (filtered["status"] == "Resolved").mean() * 100 if len(filtered) else 0
high_open = len(filtered[(filtered["severity"].isin(["High", "Critical"])) & (filtered["status"] != "Resolved")])
median_age = filtered["aging_hours"].median() if len(filtered) else 0
avg_impact = filtered["impact_score"].mean() if len(filtered) else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cases in scope", f"{len(filtered)}")
col2.metric("Open high-severity", f"{high_open}")
col3.metric("Median age", f"{median_age:.0f}h")
col4.metric("Resolved ratio", f"{resolved_ratio:.0f}%", f"{avg_impact:.1f} avg impact")

story_cols = st.columns(3)
for col, payload in zip(
    story_cols,
    [
        ("Triage", "Severity and status views let you explain how an operator quickly spots the most urgent work.", ["high signal", "priority"]),
        ("Ownership", "Aging by owner gives the page a team operations flavor rather than a pure analytics look.", ["handoff", "workload"]),
        ("Evidence", "The case queue turns the demo into something that feels concrete during an interview walkthrough.", ["review table", "audit trail"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

left, right = st.columns([1, 1])
with left:
    render_panel_title(f"{breakdown} by status", "A compact view of where the review queue is getting stuck.")
    lens_map = {"Severity": "severity", "Category": "category", "Module": "module"}
    lens = lens_map[breakdown]
    grouped = filtered.groupby(["status", lens], as_index=False).size()
    status_chart = (
        alt.Chart(grouped)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("status:N", title="Status"),
            y=alt.Y("size:Q", title="Case count"),
            color=alt.Color(
                f"{lens}:N",
                scale=alt.Scale(range=["#9fb6b0", "#d2a36d", "#b45b43", "#7d1f1f", "#395c7d"]),
                title=breakdown,
            ),
            tooltip=["status:N", f"{lens}:N", "size:Q"],
        )
        .properties(height=320)
    )
    st.altair_chart(status_chart, use_container_width=True)

with right:
    render_panel_title("Aging by owner", "Useful for showing operational follow-up and queue ownership.")
    owner_age = filtered.groupby("owner", as_index=False)["aging_hours"].mean()
    age_chart = (
        alt.Chart(owner_age)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#1f7763")
        .encode(
            x=alt.X("owner:N", title="Owner"),
            y=alt.Y("aging_hours:Q", title="Average aging hours"),
            tooltip=["owner:N", alt.Tooltip("aging_hours:Q", format=".1f")],
        )
        .properties(height=320)
    )
    st.altair_chart(age_chart, use_container_width=True)
    selected_case_id = st.selectbox("Focus case", filtered.sort_values(["severity_rank", "aging_hours"], ascending=[False, False])["case_id"].tolist())
    selected_case = filtered[filtered["case_id"] == selected_case_id].iloc[0]
    render_surface_card(
        "Focused case detail",
        f"{selected_case['category']} in {selected_case['module']} owned by {selected_case['owner']}. This case has been open for {selected_case['aging_hours']} hours with an impact score of {selected_case['impact_score']}.",
        chips=[selected_case["severity"], selected_case["status"], f"{selected_case['aging_hours']}h aged"],
    )

render_panel_title("Case queue", "Synthetic case list that mimics a real dashboard investigation table.")
table = filtered.loc[
    :,
    ["case_id", "category", "module", "severity", "status", "owner", "aging_hours", "impact_score", "created_at", "severity_rank"],
].sort_values(["severity_rank", "aging_hours", "impact_score"], ascending=[False, False, False])
table = table.drop(columns=["severity_rank"])
table["created_at"] = pd.to_datetime(table["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
st.dataframe(table, use_container_width=True, hide_index=True)
