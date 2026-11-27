"""Shared Streamlit UI helpers and visual system for SolarOps."""

from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Palette / tokens
# ---------------------------------------------------------------------------
PRIMARY = "#1E3A2F"
ACCENT = "#4F9D5A"
DARK = "#1B211E"
BG = "#F6F4EF"
CARD = "#FFFFFF"
TEXT = "#1C1F1E"
MUTED = "#5A6B63"
BORDER = "#E6E4DF"
WARNING = "#B8860B"
DANGER = "#B33A3A"
GREY = "#8A8F8C"

COLOR_ACTUAL = "#2D3748"
COLOR_PREDICTED = "#4F9D5A"
COLOR_ANOMALY = "#B33A3A"
COLOR_WARNING = "#B8860B"
COLOR_UNRELIABLE = "#8A8F8C"


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --so-primary: {PRIMARY};
            --so-accent: {ACCENT};
            --so-dark: {DARK};
            --so-bg: {BG};
            --so-card: {CARD};
            --so-text: {TEXT};
            --so-muted: {MUTED};
            --so-border: {BORDER};
            --so-warning: {WARNING};
            --so-danger: {DANGER};
            --so-grey: {GREY};
            --so-radius: 12px;
            --so-radius-sm: 8px;
        }}
        .stApp {{ background: var(--so-bg); color: var(--so-text); }}
        .stApp, .stApp p, .stApp label, .stApp span {{
            font-family: "Source Sans 3", "Source Sans Pro", system-ui, -apple-system,
                         "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        .block-container {{
            max-width: 1280px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }}
        section[data-testid="stSidebar"] {{
            background: var(--so-card);
            border-right: 1px solid var(--so-border);
        }}
        section[data-testid="stSidebar"] .block-container {{ padding-top: 1.25rem; }}
        header[data-testid="stHeader"] {{
            background: var(--so-card);
            border-bottom: 1px solid var(--so-border);
        }}
        h1 {{ color: var(--so-text); font-weight: 700; letter-spacing: -0.01em; margin-bottom: 0.25rem; }}
        h1.so-title {{ font-size: 1.75rem; margin: 0 0 0.2rem 0; }}
        .so-subtitle {{ color: var(--so-muted); font-size: 0.95rem; margin: 0 0 1.25rem 0; line-height: 1.5; }}
        div[data-testid="stMetric"] {{
            background: var(--so-card); border: 1px solid var(--so-border);
            border-radius: var(--so-radius); padding: 1rem 1.2rem;
            box-shadow: 0 1px 2px rgba(16, 24, 20, 0.04);
        }}
        div[data-testid="stMetricLabel"] {{
            color: var(--so-muted); font-size: 0.78rem; text-transform: uppercase;
            letter-spacing: 0.05em; font-weight: 600;
        }}
        div[data-testid="stMetricValue"] {{
            color: var(--so-text); font-variant-numeric: tabular-nums; font-weight: 700;
        }}
        div[data-testid="stMetricDelta"] {{ font-variant-numeric: tabular-nums; }}
        .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {{
            background: var(--so-primary); color: #FFFFFF; border: 1px solid var(--so-primary);
            border-radius: var(--so-radius-sm); font-weight: 600; padding: 0.45rem 1rem;
            transition: background 0.15s ease;
        }}
        .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {{
            background: #2A5242; border-color: #2A5242; color: #FFFFFF;
        }}
        .stButton > button[kind="secondary"] {{
            background: var(--so-card); color: var(--so-primary); border: 1px solid var(--so-border);
        }}
        .stButton > button[kind="secondary"]:hover {{ background: #F0EEE8; color: var(--so-primary); }}
        div[data-testid="stDataFrame"] {{
            border: 1px solid var(--so-border); border-radius: var(--so-radius);
            overflow: hidden; background: var(--so-card);
        }}
        details {{
            border: 1px solid var(--so-border); border-radius: var(--so-radius);
            background: var(--so-card); padding: 0.25rem 0.75rem;
        }}
        hr {{ border-color: var(--so-border); opacity: 0.6; }}
        div[data-testid="stAlert"] {{ border-radius: var(--so-radius-sm); }}
        .so-brand {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }}
        .so-brand-mark {{
            width: 28px; height: 28px; border-radius: 8px;
            background: linear-gradient(135deg, var(--so-primary), var(--so-accent));
            display: inline-flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 700; font-size: 0.85rem;
        }}
        .so-brand-name {{ font-weight: 700; font-size: 1.05rem; color: var(--so-text); letter-spacing: -0.01em; }}
        .so-context-card {{
            background: #F0EEE8; border: 1px solid var(--so-border); border-radius: var(--so-radius-sm);
            padding: 0.6rem 0.75rem; margin: 0.75rem 0 1rem 0; font-size: 0.82rem;
            color: var(--so-muted); line-height: 1.4;
        }}
        .so-context-card strong {{ color: var(--so-text); display: block; font-size: 0.85rem; margin-bottom: 0.15rem; }}
        .so-footer {{
            margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--so-border);
            color: var(--so-muted); font-size: 0.78rem; display: flex;
            justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;
        }}
        .so-empty {{
            background: var(--so-card); border: 1px dashed var(--so-border); border-radius: var(--so-radius);
            padding: 1.5rem; text-align: center; color: var(--so-muted);
        }}
        .so-chip-row {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.5rem 0 1rem 0; }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 0.25rem; }}
        .stTabs [data-baseweb="tab"] {{ border-radius: var(--so-radius-sm); padding: 0.4rem 0.9rem; }}
        .stForm {{
            border: 1px solid var(--so-border); border-radius: var(--so-radius);
            padding: 1.25rem; background: var(--so-card);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(f'<h1 class="so-title">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="so-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def render_sidebar_brand() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="so-brand">
                <span class="so-brand-mark">S</span>
                <span class="so-brand-name">SolarOps</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="so-context-card">
                <strong>Active system</strong>
                PVDAQ System 2107<br>
                Test period: 2022-07-01 → 2023-10-31
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        """
        <div class="so-footer">
            <span>SolarOps — solar performance intelligence</span>
            <span>Model v3 (LightGBM) · Streamlit</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig, title: str | None = None, height: int | None = None):
    layout = dict(
        template="plotly_white",
        height=height or 400,
        margin=dict(l=48, r=24, t=46, b=44),
        font=dict(size=12, color=TEXT, family="Source Sans 3, Source Sans Pro, system-ui, sans-serif"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=MUTED),
        ),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(size=11, color=MUTED)),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(size=11, color=MUTED)),
    )
    if title:
        layout["title"] = dict(text=title, font=dict(size=14, color=TEXT), x=0, xanchor="left")
    fig.update_layout(**layout)
    return fig