from __future__ import annotations

import streamlit as st

from src.dashboard_ui import (
    apply_theme,
    enable_screenshot_mode,
    render_filter_shell,
    render_page_hero,
    render_panel_title,
    render_surface_card,
)
from src.mock_data import get_workflow_items


st.set_page_config(page_title="Operations Workflow", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="workflow_screenshot_mode",
    inactive_note="Move to this subpage with the sidebar first, then turn on Screenshot mode for the final capture.",
    active_note="Screenshot mode is on. Try capturing the hero, owner-capacity summary, and lane board together.",
)

df = get_workflow_items().copy()

render_page_hero(
    "Operations Workflow",
    "A synthetic lane-based operations board for intake, review, validation, and release coordination. This page is useful for showing that your dashboard work also touched process design and execution, not only analytics.",
    kicker="Workflow support",
    pills=["lane view", "SLA risk", "handoff design"],
    side_label="Tracked tasks",
    side_value=str(len(df)),
    side_copy="The goal is to make the portfolio feel like it includes internal tooling, not just charting.",
)

render_filter_shell("Filters", "Focus the board on the tasks that matter most right now.")
left_filter, mid_filter, right_filter = st.columns([1, 1, 1])
with left_filter:
    priority_filter = st.multiselect(
        "Priority",
        options=["Low", "Medium", "High"],
        default=["Medium", "High"],
    )
with mid_filter:
    owner_focus = st.selectbox("Owner focus", ["All"] + sorted(df["owner"].unique().tolist()), index=0)
with right_filter:
    show_automation = st.toggle("Only show automation candidates", value=False)

secondary_left, secondary_right = st.columns([1.1, 1])
with secondary_left:
    sort_mode = st.segmented_control("Sort queue by", options=["Urgency", "Priority", "Owner"], default="Urgency")
with secondary_right:
    risk_threshold = st.slider("Risk threshold (hours)", min_value=0, max_value=24, value=6, step=2)

filtered = df[df["priority"].isin(priority_filter)]
if owner_focus != "All":
    filtered = filtered[filtered["owner"] == owner_focus]
if show_automation:
    filtered = filtered[filtered["automation_candidate"]]
if filtered.empty:
    st.warning("No workflow items match the current filters. Try adding another priority or disabling the automation-only toggle.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tasks in scope", f"{len(filtered)}")
col2.metric("SLA at risk", f"{(filtered['sla_hours_left'] < 0).sum()}")
col3.metric("Automation candidates", f"{filtered['automation_candidate'].sum()}")
col4.metric("Published", f"{(filtered['lane'] == 'Published').sum()}")

story_cols = st.columns(3)
for col, payload in zip(
    story_cols,
    [
        ("Coordinate", "The lane structure makes task state and handoff visible, which gives the demo a stronger internal-tool feel.", ["lane state", "handoff"]),
        ("Escalate", "SLA pressure and high-priority filters add operational tension that simple dashboards usually lack.", ["urgency", "risk"]),
        ("Automate", "Automation candidates help you talk about where tooling could reduce manual work over time.", ["workflow ideas", "ops efficiency"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

render_panel_title(
    "Workflow lanes",
    "A compact board designed to feel like a real internal workflow surface rather than a static report.",
)

priority_order = {"High": 0, "Medium": 1, "Low": 2}
sort_columns = {
    "Urgency": ["sla_hours_left", "priority"],
    "Priority": ["priority", "sla_hours_left"],
    "Owner": ["owner", "sla_hours_left"],
}
ascending_map = {
    "Urgency": [True, True],
    "Priority": [True, True],
    "Owner": [True, True],
}

owner_load = filtered.groupby("owner", as_index=False).agg(
    task_count=("task_id", "count"),
    at_risk=("sla_hours_left", lambda s: int((s < risk_threshold).sum())),
)
owner_load = owner_load.sort_values(["at_risk", "task_count"], ascending=[False, False])
top_left, top_right = st.columns([1.05, 0.95])
with top_left:
    render_panel_title("Owner capacity", "Who is carrying the most queue volume and time pressure.")
    st.bar_chart(owner_load.set_index("owner")[["task_count", "at_risk"]], use_container_width=True)
with top_right:
    focus_task_id = st.selectbox("Focus task", filtered.sort_values("sla_hours_left")["task_id"].tolist())
    focus_task = filtered[filtered["task_id"] == focus_task_id].iloc[0]
    render_surface_card(
        "Focused task detail",
        f"{focus_task['task_type']} owned by {focus_task['owner']} currently sits in {focus_task['lane']} with {focus_task['sla_hours_left']} hours left. This is useful for explaining workflow triage and handoff logic.",
        chips=[focus_task["priority"], focus_task["lane"], "automation candidate" if focus_task["automation_candidate"] else "manual path"],
    )

lanes = ["Intake", "Review", "Validate", "Published"]
lane_cols = st.columns(len(lanes))
for col, lane in zip(lane_cols, lanes):
    with col:
        lane_df = filtered[filtered["lane"] == lane].copy()
        if sort_mode == "Priority":
            lane_df["priority_sort"] = lane_df["priority"].map(priority_order)
            lane_df = lane_df.sort_values(["priority_sort", "sla_hours_left"], ascending=[True, True])
        else:
            lane_df = lane_df.sort_values(sort_columns[sort_mode], ascending=ascending_map[sort_mode])
        st.markdown(
            f"""
            <div class="lane-card">
                <div class="lane-title">{lane}</div>
                <p>{len(lane_df)} tasks currently visible</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for _, row in lane_df.head(6).iterrows():
            risk = "At risk" if row["sla_hours_left"] < risk_threshold else f"{row['sla_hours_left']}h left"
            st.markdown(
                f"""
                <div class="module-card" style="margin-top:0.7rem;">
                    <div class="module-title">{row['task_type']}</div>
                    <div class="module-body">{row['summary']}</div>
                    <div class="chip">{row['task_id']}</div>
                    <div class="chip">{row['owner']}</div>
                    <div class="chip">{row['priority']}</div>
                    <div class="chip">{risk}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

render_panel_title("Detailed queue", "Sortable queue for a more realistic portfolio snapshot.")
st.dataframe(
    filtered.sort_values("sla_hours_left").loc[:, ["task_id", "lane", "task_type", "owner", "priority", "sla_hours_left", "automation_candidate"]],
    use_container_width=True,
    hide_index=True,
)
