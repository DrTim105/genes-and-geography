# streamlit_app/components.py
"""Reusable HTML components for the app."""
 
import streamlit as st
 
def hero(eyebrow, title_text, accent_word, subtitle, meta):
    """Render the hero section at the top of the page.
 
    Parameters
    ----------
    eyebrow : str    Small uppercase label above the title.
    title_text : str    Main title; pass the part that should be highlighted as 'accent_word'.
    accent_word : str    The word/phrase to highlight in accent colour.
    subtitle : str    One sentence below the title.
    meta : str    Mono-spaced meta info row at the bottom.
    """
    # Split title around the accent word so we can wrap it in a styled span
    title_html = title_text.replace(
        accent_word,
        f'<span class="accent">{accent_word}</span>'
    )
    html = f"""
    <div class="hero">
        <div class="hero-eyebrow">{eyebrow}</div>
        <h1 class="hero-title">{title_html}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        <div class="hero-meta">{meta}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def kpi_row(items):
    """Render a row of KPI cards."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{item['value']}</div>
            <div class="kpi-label">{item['label']}</div>
            <div class="kpi-sub">{item['sub']}</div>
        </div>
        """, unsafe_allow_html=True)
 
 
def section_header(eyebrow, title, lead):
    """Eyebrow + title + lead paragraph above each section."""
    html = f"""
    <div class="section-eyebrow">{eyebrow}</div>
    <h2 class="section-title">{title}</h2>
    <p class="section-lead">{lead}</p>
    """
    st.markdown(html, unsafe_allow_html=True)
 
 
def callout(label, body):
    """Highlighted callout block for key findings or quotes."""
    html = f"""
    <div class="callout">
        <div class="callout-label">{label}</div>
        <div class="callout-body">{body}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
 
 
def footer():
    """Site footer."""
    html = """
    <div class="app-footer">
        Built by <a href="https://github.com/DrTim105">Dr. Salihu Timothy</a>
        · Source on
        <a href="https://github.com/DrTim105/genes-and-geography">GitHub</a>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
