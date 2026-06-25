from __future__ import annotations

import altair as alt
import streamlit as st

from src.dashboard_ui import (
    apply_theme,
    enable_screenshot_mode,
    render_filter_shell,
    render_page_hero,
    render_panel_title,
    render_surface_card,
)
from src.mock_data import get_universe_records


st.set_page_config(page_title="Universe Explorer", layout="wide")
apply_theme()
enable_screenshot_mode(
    toggle_key="universe_screenshot_mode",
    inactive_note="Use the sidebar to pick this page, then switch on Screenshot mode to capture the explorer cleanly.",
    active_note="Screenshot mode is on. This page frames well with the hero, coverage chart, and focused instrument panel.",
)

df = get_universe_records()

render_page_hero(
    "Universe Explorer",
    "A synthetic explorer for searchable entities, coverage gaps, and readiness scoring. This page leans closer to the kind of reference-data or coverage workflow that makes an internal dashboard feel broad and useful.",
    kicker="Search and coverage",
    pills=["entity search", "coverage lens", "gap analysis"],
    side_label="Universe size",
    side_value=str(len(df)),
    side_copy="This module is useful for showing searchable metadata, filters, and coverage logic without exposing real instruments or internal labels.",
)

render_filter_shell("Filters", "Use the explorer like a mini workbench for reference coverage and readiness checks.")
row1, row2, row3 = st.columns([1.2, 1, 1])
with row1:
    search = st.text_input("Search name or ID", placeholder="Type an instrument name or UNI id")
with row2:
    asset_filter = st.multiselect(
        "Asset class",
        options=sorted(df["asset_class"].unique().tolist()),
        default=sorted(df["asset_class"].unique().tolist()),
    )
with row3:
    region_filter = st.multiselect(
        "Region",
        options=sorted(df["region"].unique().tolist()),
        default=sorted(df["region"].unique().tolist()),
    )

row4, row5, row6 = st.columns([1, 1, 1])
with row4:
    coverage_filter = st.multiselect(
        "Coverage status",
        options=["Ready", "Partial", "Missing"],
        default=["Ready", "Partial", "Missing"],
    )
with row5:
    lifecycle_filter = st.multiselect(
        "Lifecycle",
        options=sorted(df["lifecycle"].unique().tolist()),
        default=sorted(df["lifecycle"].unique().tolist()),
    )
with row6:
    only_hedge_ready = st.toggle("Only hedge-ready", value=False)

secondary_left, secondary_mid, secondary_right = st.columns([1, 1.05, 0.95])
with secondary_left:
    sort_metric = st.segmented_control("Rank candidates by", options=["readiness_score", "mapping_gaps", "liquidity_score"], default="mapping_gaps")
with secondary_mid:
    scatter_y = st.segmented_control("Scatter y-axis", options=["readiness_score", "avg_daily_turnover_m", "mapping_gaps"], default="readiness_score")
with secondary_right:
    top_n = st.slider("Show top N weakest", min_value=8, max_value=40, value=16, step=4)

filtered = df[
    df["asset_class"].isin(asset_filter)
    & df["region"].isin(region_filter)
    & df["coverage_status"].isin(coverage_filter)
    & df["lifecycle"].isin(lifecycle_filter)
]
if search:
    needle = search.lower()
    filtered = filtered[
        filtered["display_name"].str.lower().str.contains(needle)
        | filtered["instrument_id"].str.lower().str.contains(needle)
    ]
if only_hedge_ready:
    filtered = filtered[filtered["hedge_ready"]]
if filtered.empty:
    st.warning("No instruments match the current filters. Try broadening the search or re-enabling more coverage states.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Instruments in scope", f"{len(filtered)}")
col2.metric("Average readiness", f"{filtered['readiness_score'].mean():.1f}")
col3.metric("Total mapping gaps", f"{filtered['mapping_gaps'].sum():.0f}")
col4.metric("Regions represented", f"{filtered['region'].nunique()}")

story_cols = st.columns(3)
for col, payload in zip(
    story_cols,
    [
        ("Search", "Search plus metadata filters gives the page a real explorer feel instead of a decorative chart wall.", ["lookup", "filters"]),
        ("Prioritize", "Coverage status and mapping gaps create a natural backlog and story about what to fix next.", ["gaps", "coverage"]),
        ("Assess", "Readiness and liquidity scores help the page feel analytical rather than just reference-data oriented.", ["scoring", "readiness"]),
    ],
):
    with col:
        render_surface_card(payload[0], payload[1], chips=payload[2])

left, right = st.columns([1.08, 0.92])
with left:
    render_panel_title("Coverage by region", "A compact regional coverage view for the filtered universe.")
    coverage_by_region = filtered.groupby(["region", "coverage_status"], as_index=False).size()
    coverage_chart = (
        alt.Chart(coverage_by_region)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("region:N", title="Region"),
            y=alt.Y("size:Q", title="Instrument count"),
            color=alt.Color(
                "coverage_status:N",
                scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]),
                title="Coverage",
            ),
            tooltip=["region:N", "coverage_status:N", "size:Q"],
        )
        .properties(height=330)
    )
    st.altair_chart(coverage_chart, use_container_width=True)

with right:
    render_panel_title("Readiness versus liquidity", "A score view that makes the explorer feel more analytical.")
    scatter = (
        alt.Chart(filtered)
        .mark_circle(size=180)
        .encode(
            x=alt.X("liquidity_score:Q", title="Liquidity score"),
            y=alt.Y(f"{scatter_y}:Q", title=scatter_y.replace("_", " ").title()),
            color=alt.Color(
                "coverage_status:N",
                scale=alt.Scale(range=["#1f7763", "#d98d48", "#b55443"]),
                title="Coverage",
            ),
            tooltip=["instrument_id:N", "display_name:N", "region:N", "asset_class:N", "readiness_score:Q", "liquidity_score:Q", "mapping_gaps:Q", "avg_daily_turnover_m:Q"],
        )
        .properties(height=330)
    )
    st.altair_chart(scatter, use_container_width=True)

render_panel_title("Explorer table", "Searchable synthetic universe with enough detail to support a product walkthrough.")
ascending = sort_metric != "mapping_gaps"
display = filtered.sort_values([sort_metric, "mapping_gaps"], ascending=[ascending, False]).loc[
    :,
    ["instrument_id", "display_name", "asset_class", "region", "sector", "coverage_status", "readiness_score", "liquidity_score", "mapping_gaps", "hedge_ready"],
]
highlight = display.head(top_n)
detail_left, detail_right = st.columns([1.05, 0.95])
with detail_left:
    st.dataframe(display, use_container_width=True, hide_index=True)
with detail_right:
    focus_instrument = st.selectbox("Focus instrument", highlight["instrument_id"].tolist())
    selected = filtered[filtered["instrument_id"] == focus_instrument].iloc[0]
    render_surface_card(
        "Focused instrument detail",
        f"{selected['display_name']} is a {selected['asset_class']} in {selected['region']} with {selected['coverage_status'].lower()} coverage and a readiness score of {selected['readiness_score']}.",
        chips=[selected["benchmark_family"], selected["lifecycle"], f"{selected['mapping_gaps']} gaps"],
    )
    weakest = highlight.loc[:, ["instrument_id", "display_name", "coverage_status", "mapping_gaps", "readiness_score"]]
    st.dataframe(weakest, use_container_width=True, hide_index=True)
