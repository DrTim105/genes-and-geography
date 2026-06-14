# streamlit_app/styles.py 
import streamlit as st
 
CSS = """
<style>
    /* ----- Google Fonts ----- */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
 
    /* ----- Design tokens (variables) ----- */
    :root {
        --bg-primary: #0A1929;
        --bg-secondary: #0F1F30;
        --bg-card: rgba(255, 255, 255, 0.03);
        --bg-card-hover: rgba(255, 255, 255, 0.06);
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-medium: rgba(255, 255, 255, 0.15);
        --text-primary: #F5F7FA;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-orange: #D4600A;
        --accent-orange-soft: rgba(212, 96, 10, 0.15);
        --accent-glow: rgba(212, 96, 10, 0.4);
        --accent-blue: #4A90E2;
        --accent-teal: #2DD4BF;
    }
 
    /* ----- Reset Streamlit defaults ----- */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }
 
    /* Hide the default Streamlit header/menu */
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { display: none; }
    footer { display: none; }
    #MainMenu { display: none; }
 
    /* Body & font baseline */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        color: var(--text-primary);
    }
 
    /* Headings use Space Grotesk */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }
 
    /* ----- Hero section ----- */
    .hero {
        padding: 4rem 0 3rem 0;
        text-align: center;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 3rem;
    }
    .hero-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--accent-orange);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.04em;
        margin: 0;
        color: var(--text-primary);
    }
    .hero-title .accent {
        color: var(--accent-orange);
        text-shadow: 0 0 40px var(--accent-glow);
    }
    .hero-subtitle, .hero-subtitle p, div.hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.25rem !important;
        color: var(--text-secondary) !important;
        max-width: 640px !important;
        margin: 1.5rem auto 0 auto !important;
        line-height: 1.5 !important;
        font-weight: 300 !important;
        text-align: center !important;
    }
    .hero-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 2rem;
    }
 
    /* ----- KPI cards ----- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0 3rem 0;
    }
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
    }
    .kpi-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-medium);
        transform: translateY(-2px);
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: var(--accent-orange);
        text-shadow: 0 0 30px var(--accent-glow);
        line-height: 1;
    }
    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 0.75rem;
    }
    .kpi-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 300;
    }
 
    /* ----- Section eyebrow & headers ----- */
    .section-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--accent-orange);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 0.5rem;
    }
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 0.75rem;
    }
    .section-lead {
        font-size: 1.1rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 720px;
    }
 
    /* ----- Callout blocks ----- */
    .callout {
        background: var(--accent-orange-soft);
        border-left: 3px solid var(--accent-orange);
        border-radius: 4px;
        padding: 1.5rem 1.75rem;
        margin: 2rem 0;
    }
    .callout-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent-orange);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 0.5rem;
    }
    .callout-body {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 1rem;
    }
 
    /* ----- Restyle Streamlit's built-in tabs ----- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 0;
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--text-secondary) !important;
        padding: 0.5rem 0 !important;
        margin: 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-orange) !important;
        border-bottom: 2px solid var(--accent-orange) !important;
    }
 
    /* ----- Restyle sliders ----- */
    .stSlider [data-baseweb="slider"] > div > div > div > div {
        background: var(--accent-orange) !important;
    }
 
    /* ----- Restyle the multiselect pills ----- */
    .stMultiSelect [data-baseweb="tag"] {
        background: var(--accent-orange-soft) !important;
        color: var(--accent-orange) !important;
        border: 1px solid var(--accent-orange) !important;
    }
 
    /* ----- Code blocks ----- */
    code, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
        background: var(--bg-secondary) !important;
        color: var(--accent-teal) !important;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
 
    /* ----- Footer ----- */
    .app-footer {
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border-subtle);
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
    }
    .app-footer a {
        color: var(--accent-orange);
        text-decoration: none;
    }
</style>
"""
 
def inject_css():
    """Call once at the top of app.py to apply the design system."""
    st.markdown(CSS, unsafe_allow_html=True)