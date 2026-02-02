import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    /* ---------- Base ---------- */
    body {
        background-color: #0b0f1a;
        color: #e5e7eb;
    }

    /* ---------- Headings ---------- */
    h1, h2, h3 {
        color: #f9fafb;
    }

    /* ---------- Labels vs Values ---------- */
    .label {
        color: #38bdf8;
        font-weight: 500;
        margin-bottom: 2px;
    }

    .value {
        color: #9ca3af;
        font-weight: 600;
    }

    /* ---------- Risk Colors ---------- */
    .risk-high {
        color: #ef4444;
        font-weight: 700;
    }

    .risk-medium {
        color: #f59e0b;
        font-weight: 700;
    }

    .risk-low {
        color: #22c55e;
        font-weight: 700;
    }

    /* ---------- Metric Cards ---------- */
    .metric-card {
        background: linear-gradient(145deg, #111827, #020617);
        padding: 10px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-top: 28px;
    }

    .metric-title {
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 36px;
        font-weight: 800;
    }

    /* ---------- Info / Warning / Success ---------- */
    .stAlert {
        border-radius: 12px;
    }

    /* ---------- Tabs ---------- */
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)
