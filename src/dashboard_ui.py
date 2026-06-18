from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg-base: #f6f1e8;
                --bg-soft: #f7faf8;
                --bg-card: rgba(255, 255, 255, 0.82);
                --bg-card-strong: rgba(255, 255, 255, 0.92);
                --text-main: #102028;
                --text-soft: #46606a;
                --text-muted: #6a7f79;
                --line-soft: rgba(17, 36, 45, 0.10);
                --line-strong: rgba(17, 36, 45, 0.18);
                --accent: #1f7763;
                --accent-soft: #e1f3ee;
                --accent-warm: #d98d48;
                --shadow-soft: 0 10px 30px rgba(17, 36, 45, 0.05);
                --shadow-strong: 0 24px 70px rgba(17, 36, 45, 0.10);
            }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(184, 222, 214, 0.28), transparent 26%),
                    radial-gradient(circle at top right, rgba(242, 208, 162, 0.16), transparent 22%),
                    linear-gradient(180deg, var(--bg-base) 0%, var(--bg-soft) 55%, #edf7f4 100%);
            }
            .block-container {
                padding-top: 1.4rem;
                padding-bottom: 3.4rem;
                max-width: 1220px;
            }
            html, body, [class*="css"]  {
                font-family: Avenir Next, ui-sans-serif, system-ui, sans-serif;
            }
            h1, h2, h3 {
                color: var(--text-main);
                letter-spacing: -0.02em;
            }
            [data-testid="stSidebar"] {
                display: block !important;
                background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(242,247,245,0.96));
                border-right: 1px solid var(--line-soft);
            }
            header[data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stDecoration"] {
                display: block !important;
            }
            [data-testid="stSidebarNav"] {
                padding-top: 1rem;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Portfolio Demo";
                display: block;
                margin: 0 0 1rem;
                color: var(--text-main);
                font-size: 1.05rem;
                font-weight: 700;
                letter-spacing: -0.01em;
            }
            [data-testid="stSidebarNav"] a {
                border-radius: 14px;
                margin-bottom: 0.25rem;
                color: var(--text-soft);
            }
            [data-testid="stSidebarNav"] a:hover {
                background: rgba(31, 119, 99, 0.08);
                color: var(--text-main);
            }
            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background: rgba(31, 119, 99, 0.12);
                color: var(--text-main);
                font-weight: 700;
            }
            .hero-shell {
                position: relative;
                overflow: hidden;
                padding: 1.7rem 1.8rem;
                border: 1px solid var(--line-soft);
                border-radius: 28px;
                background:
                    radial-gradient(circle at 80% 0%, rgba(217, 141, 72, 0.14), transparent 24%),
                    linear-gradient(135deg, rgba(255,255,255,0.78), rgba(233, 245, 241, 0.92));
                box-shadow: var(--shadow-strong);
                margin-bottom: 1rem;
            }
            .hero-shell::after {
                content: "";
                position: absolute;
                right: -40px;
                top: -48px;
                width: 180px;
                height: 180px;
                border-radius: 999px;
                background: radial-gradient(circle, rgba(31,119,99,0.16), rgba(31,119,99,0.00) 66%);
                pointer-events: none;
            }
            .page-hero {
                margin-bottom: 1.15rem;
            }
            .hero-layout {
                display: grid;
                grid-template-columns: 1.35fr 0.72fr;
                gap: 1rem;
                align-items: end;
            }
            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-muted);
                font-size: 0.78rem;
                margin-bottom: 0.35rem;
            }
            .hero-title {
                font-size: 2.5rem;
                line-height: 1.02;
                font-weight: 700;
                color: var(--text-main);
                margin-bottom: 0.55rem;
            }
            .hero-copy {
                max-width: 54rem;
                color: #37505b;
                line-height: 1.65;
                font-size: 1rem;
            }
            .hero-side {
                border: 1px solid rgba(16, 32, 40, 0.10);
                border-radius: 22px;
                background: rgba(255,255,255,0.62);
                padding: 1rem 1rem 0.95rem;
                backdrop-filter: blur(8px);
            }
            .hero-side-label {
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-muted);
                font-size: 0.72rem;
                margin-bottom: 0.25rem;
            }
            .hero-side-value {
                color: var(--text-main);
                font-size: 2rem;
                line-height: 1;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }
            .hero-side-copy {
                color: var(--text-soft);
                font-size: 0.92rem;
                line-height: 1.55;
            }
            .hero-pill-row {
                margin-top: 0.9rem;
            }
            .hero-pill {
                display: inline-block;
                margin: 0 0.35rem 0.35rem 0;
                padding: 0.24rem 0.65rem;
                border-radius: 999px;
                background: rgba(31,119,99,0.10);
                color: var(--accent);
                font-size: 0.78rem;
                font-weight: 600;
            }
            .metric-strip {
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 0.8rem;
                margin: 0.5rem 0 1.2rem;
            }
            .metric-card {
                padding: 1rem 1rem 0.95rem;
                border-radius: 20px;
                background: var(--bg-card);
                border: 1px solid var(--line-soft);
                box-shadow: var(--shadow-soft);
            }
            .metric-label {
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.06em;
                font-size: 0.72rem;
                margin-bottom: 0.35rem;
            }
            .metric-value {
                color: var(--text-main);
                font-size: 1.55rem;
                font-weight: 700;
                line-height: 1.1;
            }
            .metric-delta {
                color: var(--accent);
                margin-top: 0.28rem;
                font-size: 0.82rem;
            }
            .filter-shell {
                border: 1px solid var(--line-soft);
                border-radius: 24px;
                padding: 0.9rem 1rem 0.35rem;
                background: rgba(255,255,255,0.62);
                box-shadow: var(--shadow-soft);
                margin-bottom: 1rem;
            }
            .filter-kicker {
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.72rem;
                margin-bottom: 0.2rem;
            }
            .panel-title {
                margin-top: 0.6rem;
                font-size: 1.15rem;
                font-weight: 700;
                color: var(--text-main);
            }
            .panel-copy {
                color: var(--text-soft);
                margin-bottom: 0.7rem;
            }
            .surface-card {
                border: 1px solid var(--line-soft);
                background: var(--bg-card-strong);
                border-radius: 24px;
                padding: 1rem 1rem 0.95rem;
                box-shadow: var(--shadow-soft);
                height: 100%;
            }
            .surface-title {
                color: var(--text-main);
                font-size: 1rem;
                font-weight: 700;
                margin-bottom: 0.28rem;
            }
            .surface-copy {
                color: var(--text-soft);
                line-height: 1.55;
                font-size: 0.92rem;
                margin: 0;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.8rem;
                margin-bottom: 1rem;
            }
            .feature-card, .module-card, .lane-card {
                border: 1px solid var(--line-soft);
                background: rgba(255,255,255,0.84);
                border-radius: 22px;
                padding: 1rem;
                box-shadow: var(--shadow-soft);
            }
            .feature-card p, .module-body, .lane-card p {
                color: var(--text-soft);
                line-height: 1.55;
                margin: 0.35rem 0 0;
                font-size: 0.94rem;
            }
            .module-title, .lane-title {
                color: var(--text-main);
                font-size: 1.05rem;
                font-weight: 700;
            }
            .chip {
                display: inline-block;
                padding: 0.18rem 0.52rem;
                border-radius: 999px;
                background: var(--accent-soft);
                color: #1b5047;
                margin: 0.15rem 0.22rem 0 0;
                font-size: 0.76rem;
            }
            .status-chip {
                display: inline-block;
                padding: 0.2rem 0.56rem;
                border-radius: 999px;
                background: rgba(217, 141, 72, 0.12);
                color: #8b5322;
                margin-right: 0.32rem;
                font-size: 0.75rem;
                font-weight: 600;
            }
            .stButton button, .stDownloadButton button {
                border-radius: 14px;
                border: 1px solid var(--line-soft);
                background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(241,247,245,0.98));
                color: var(--text-main);
                font-weight: 600;
                box-shadow: var(--shadow-soft);
            }
            .stButton button:hover, .stDownloadButton button:hover {
                border-color: rgba(31, 119, 99, 0.28);
                color: var(--accent);
            }
            .stMultiSelect, .stSelectbox, .stTextInput, .stSlider {
                background: transparent;
            }
            div[data-baseweb="select"] > div,
            div[data-baseweb="base-input"] > div,
            [data-testid="stDateInput"] > div > div {
                border-radius: 14px !important;
                border: 1px solid var(--line-soft) !important;
                background: rgba(255,255,255,0.86) !important;
                box-shadow: none !important;
            }
            [data-baseweb="tag"] {
                background: var(--accent-soft) !important;
                border-radius: 999px !important;
                color: var(--accent) !important;
            }
            div[data-testid="stMetric"] {
                padding: 0.9rem 1rem;
                border: 1px solid var(--line-soft);
                border-radius: 18px;
                background: rgba(255,255,255,0.82);
                box-shadow: var(--shadow-soft);
            }
            div[data-testid="stMetric"] label p {
                color: var(--text-muted) !important;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                font-size: 0.72rem;
                font-weight: 700;
            }
            div[data-testid="stMetricValue"] {
                color: var(--text-main) !important;
            }
            div[data-testid="stDataFrame"] {
                border-radius: 18px;
                overflow: hidden;
                border: 1px solid var(--line-soft);
                box-shadow: var(--shadow-soft);
            }
            [data-baseweb="tab-list"] {
                gap: 0.35rem;
                margin-bottom: 0.6rem;
            }
            [data-baseweb="tab"] {
                border-radius: 999px;
                background: rgba(255,255,255,0.68);
                border: 1px solid transparent;
                padding: 0.45rem 0.9rem;
            }
            [data-baseweb="tab"][aria-selected="true"] {
                background: rgba(31,119,99,0.12);
                border-color: rgba(31,119,99,0.20);
                color: var(--accent);
            }
            div[data-testid="stMetric"] {
                padding: 0.85rem 1rem;
            }
            @media (max-width: 1100px) {
                .metric-strip, .feature-grid, .hero-layout {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }
            @media (max-width: 760px) {
                .metric-strip, .feature-grid, .hero-layout {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_strip(items: list[dict[str, str]]) -> None:
    body = "".join(
        (
            f'<div class="metric-card">'
            f'<div class="metric-label">{item["label"]}</div>'
            f'<div class="metric-value">{item["value"]}</div>'
            f'<div class="metric-delta">{item["delta"]}</div>'
            f"</div>"
        )
        for item in items
    )
    st.markdown(f"<div class='metric-strip'>{body}</div>", unsafe_allow_html=True)


def render_panel_title(title: str, copy: str | None = None) -> None:
    st.markdown(f"<div class='panel-title'>{title}</div>", unsafe_allow_html=True)
    if copy:
        st.markdown(f"<div class='panel-copy'>{copy}</div>", unsafe_allow_html=True)


def render_page_hero(
    title: str,
    subtitle: str,
    *,
    kicker: str = "Portfolio-safe module",
    pills: list[str] | None = None,
    side_label: str | None = None,
    side_value: str | None = None,
    side_copy: str | None = None,
) -> None:
    pill_markup = ""
    if pills:
        pill_markup = (
            "<div class='hero-pill-row'>"
            + "".join(f"<span class='hero-pill'>{item}</span>" for item in pills)
            + "</div>"
        )

    side_markup = ""
    if side_label or side_value or side_copy:
        side_markup = (
            '<div class="hero-side">'
            f'<div class="hero-side-label">{side_label or ""}</div>'
            f'<div class="hero-side-value">{side_value or ""}</div>'
            f'<div class="hero-side-copy">{side_copy or ""}</div>'
            "</div>"
        )

    html = (
        '<div class="hero-shell page-hero">'
        '<div class="hero-layout">'
        "<div>"
        f'<div class="hero-kicker">{kicker}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-copy">{subtitle}</div>'
        f"{pill_markup}"
        "</div>"
        f"<div>{side_markup}</div>"
        "</div>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def render_filter_shell(title: str, subtitle: str | None = None) -> None:
    copy = f"<div class='panel-copy' style='margin-bottom:0;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div class="filter-shell">
            <div class="filter-kicker">{title}</div>
            {copy}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_surface_card(title: str, body: str, *, chips: list[str] | None = None) -> None:
    chips_markup = ""
    if chips:
        chips_markup = (
            "<div style='margin-top:0.5rem;'>"
            + "".join(f"<span class='chip'>{chip}</span>" for chip in chips)
            + "</div>"
        )
    html = (
        '<div class="surface-card">'
        f'<div class="surface-title">{title}</div>'
        f'<p class="surface-copy">{body}</p>'
        f"{chips_markup}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
