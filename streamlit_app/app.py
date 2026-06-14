# streamlit_app/app.py
"""
Genes and Geography Explorer — interactive Streamlit app.
Run locally with:  streamlit run streamlit_app/app.py
"""
 
import json
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
 
from styles import inject_css
from components import hero, kpi_row, section_header, callout, footer
 
# ---------------------------------------------------------------- page config
st.set_page_config(
    page_title="Genes and Geography Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)
inject_css()
 
# ---------------------------------------------------------------- data loading
@st.cache_data
def load_samples():
    return pd.read_csv("streamlit_app/data/samples.csv")
 
@st.cache_data
def load_top_aims():
    return pd.read_csv("streamlit_app/data/top_aims.csv")
 
@st.cache_data
def load_aims_pcas():
    with open("streamlit_app/data/aims_pcas.json") as f:
        return json.load(f)
 
@st.cache_data
def load_stats():
    with open("streamlit_app/data/stats.json") as f:
        return json.load(f)
 
samples = load_samples()
top_aims = load_top_aims()
aims_pcas = load_aims_pcas()
stats = load_stats()
 
# ---------------------------------------------------------------- altair theme
def dark_theme():
    return {
        "config": {
            "background": "transparent",
            "view": {"stroke": "transparent"},
            "axis": {
                "labelColor": "#94A3B8",
                "titleColor": "#94A3B8",
                "labelFont": "Inter",
                "titleFont": "Inter",
                "labelFontSize": 12,
                "titleFontSize": 13,
                "gridColor": "rgba(255,255,255,0.05)",
                "domainColor": "rgba(255,255,255,0.1)",
                "tickColor": "rgba(255,255,255,0.1)"
            },
            "legend": {
                "labelColor": "#94A3B8",
                "titleColor": "#F5F7FA",
                "labelFont": "Inter",
                "titleFont": "Inter"
            },
            "title": {
                "color": "#F5F7FA",
                "font": "Space Grotesk",
                "fontSize": 18,
                "subtitleColor": "#94A3B8",
                "subtitleFont": "Inter"
            }
        }
    }
 
alt.themes.register("dark_editorial", dark_theme)
alt.themes.enable("dark_editorial")
 
SUPERPOP_COLORS = alt.Scale(
    domain=["African Ancestry", "European Ancestry",
            "East Asian Ancestry", "American Ancestry"],
    range=["#D4600A", "#4A90E2", "#E64C66", "#2DD4BF"]
)
 
# ============================================================= HERO
hero(
    eyebrow="1000 Genomes · Chromosome 22 · Phase 1",
    title_text=f"Genes and Geography",
    accent_word="Geography",
    subtitle="Reading human history from DNA — and the variants that explain "
             "why one-size-fits-all medicine doesn't work.",
    meta=f"{stats['n_samples']:,} INDIVIDUALS · {stats['n_populations']} POPULATIONS · "
         f"{stats['n_variants']:,} VARIANTS · {stats['n_superpopulations']} CONTINENTS"
)
 
# ============================================================= KPI ROW
kpi_row([
    {
        "value": f"{stats['diversity_ratio']:.2f}×",
        "label": "African diversity",
        "sub": "Within-group variability vs Europeans on chr 22"
    },
    {
        "value": "50",
        "label": "Variants needed",
        "sub": f"to recover global structure from {stats['n_variants']:,}"
    },
    {
        "value": "70k yr",
        "label": "Visible bottleneck",
        "sub": "Time since the out-of-Africa migration"
    }
])
 
# ============================================================= TABS
tab_global, tab_africa, tab_diversity, tab_aims, tab_method = st.tabs([
    "The Global View",
    "Within Africa",
    "The Bottleneck",
    "The Variants Doing the Work",
    "Method & Caveats"
])
 
# ============================================================= TAB 1 — GLOBAL
with tab_global:
    section_header(
        eyebrow="01 · Population structure",
        title="Four continents emerge from chromosome 22 alone",
        lead="Principal component analysis compresses ~5,000 genetic variants "
             "into two axes. Without being told where anyone is from, the "
             "algorithm separates samples into four continental clusters."
    )
 
    # Interactive filter
    all_supers = sorted(samples['Superpopulation name'].dropna().unique())
    selected = st.multiselect(
        "Filter by ancestry group",
        options=all_supers,
        default=all_supers,
        help="Hide or show specific groups to see how each contributes to the plot."
    )
 
    df_view = samples[samples['Superpopulation name'].isin(selected)]
 
    # Build the chart
    chart = alt.Chart(df_view).mark_circle(size=50, opacity=0.75).encode(
        x=alt.X('pc1_global:Q',
                title='PC1 — captures 8.25% of variance',
                scale=alt.Scale(zero=False)),
        y=alt.Y('pc2_global:Q',
                title='PC2 — captures 5.41% of variance',
                scale=alt.Scale(zero=False)),
        color=alt.Color('Superpopulation name:N', scale=SUPERPOP_COLORS,
                        legend=alt.Legend(title="Ancestry group", orient='right')),
        tooltip=['Sample:N', 'Population name:N', 'Superpopulation name:N',
                 alt.Tooltip('pc1_global:Q', format='.2f', title='PC1'),
                 alt.Tooltip('pc2_global:Q', format='.2f', title='PC2')]
    ).properties(height=520).interactive()
 
    st.altair_chart(chart, use_container_width=True)
 
    callout("KEY OBSERVATION",
            "The African cluster (orange) is visibly more spread out than the others. "
            "That isn't a plotting artefact — it's the within-population genetic "
            "diversity difference made visible. African populations have had ~300,000 "
            "years to accumulate variation. Non-Africans descend from a much smaller "
            "founding group that left ~70,000 years ago.")
 
# ============================================================= TAB 2 — AFRICA
with tab_africa:
    section_header(
        eyebrow="02 · The project's unique angle",
        title="Geography mirrors DNA within Africa, too",
        lead="The same method applied only to African samples recovers "
             "real geographic structure — Nigeria (YRI) and Kenya (LWK) "
             "separate cleanly, while African-American samples (ASW) "
             "smear toward Europeans because of documented post-1500 admixture."
    )
 
    df_afr = samples[samples['Superpopulation name'] == 'African Ancestry'].dropna(
        subset=['pc1_afr', 'pc2_afr'])
 
    pop_colors = alt.Scale(
        domain=['YRI', 'LWK', 'ASW'],
        range=['#D4600A', '#4A90E2', '#94A3B8']
    )
 
    chart_afr = alt.Chart(df_afr).mark_circle(size=70, opacity=0.85).encode(
        x=alt.X('pc1_afr:Q', title='PC1', scale=alt.Scale(zero=False)),
        y=alt.Y('pc2_afr:Q', title='PC2', scale=alt.Scale(zero=False)),
        color=alt.Color('Population code:N', scale=pop_colors,
                        legend=alt.Legend(title="Population", orient='right')),
        tooltip=['Sample:N', 'Population name:N',
                 alt.Tooltip('pc1_afr:Q', format='.2f'),
                 alt.Tooltip('pc2_afr:Q', format='.2f')]
    ).properties(height=520).interactive()
 
    st.altair_chart(chart_afr, use_container_width=True)
 
    cols = st.columns(3)
    populations = [
        ("YRI", "Yoruba in Ibadan, Nigeria",
         "West African; the project author's ancestral population."),
        ("LWK", "Luhya in Webuye, Kenya",
         "East African; separates from YRI on PC2 — real geographic distance."),
        ("ASW", "African-American (SW USA)",
         "Admixed; smears toward Europeans on PC1 due to post-1500 ancestry mixing.")
    ]
    for col, (code, name, desc) in zip(cols, populations):
        col.markdown(f"""
        <div class="kpi-card" style="text-align:left;">
            <div style="font-family:'JetBrains Mono'; color:#D4600A; font-size:0.8rem;
                        letter-spacing:0.15em;">{code}</div>
            <div style="font-family:'Space Grotesk'; font-size:1.1rem; font-weight:500;
                        margin-top:0.4rem;">{name}</div>
            <div style="color:#94A3B8; font-size:0.9rem; margin-top:0.6rem;
                        line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
 
# ============================================================= TAB 3 — DIVERSITY
with tab_diversity:
    section_header(
        eyebrow="03 · The Out-of-Africa Bottleneck",
        title=f"Africans carry {(stats['diversity_ratio']-1)*100:.0f}% more "
              "diversity, on this chromosome",
        lead="When a small group left Africa ~70,000 years ago, they carried "
             "only a subset of African genetic variation. Every non-African "
             "alive today descends from that handful. The diversity gap remains "
             "visible in the genome today — and matters for medicine."
    )
 
    div_df = pd.DataFrame({
        'Population': ['European', 'African'],
        'Diversity': [stats['eur_diversity'], stats['afr_diversity']]
    })
 
    chart_div = alt.Chart(div_df).mark_bar(
        cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=140
    ).encode(
        x=alt.X('Population:N', axis=alt.Axis(labelFontSize=14)),
        y=alt.Y('Diversity:Q', title='Mean allele-count std dev'),
        color=alt.Color('Population:N',
            scale=alt.Scale(domain=['European', 'African'],
                            range=['#4A90E2', '#D4600A']),
            legend=None)
    ).properties(height=420)
 
    labels = chart_div.mark_text(
        baseline='top', dy=-30, fontSize=18, fontWeight='bold',
        color='white', font='Space Grotesk'
    ).encode(text=alt.Text('Diversity:Q', format='.4f'))
 
    st.altair_chart(chart_div + labels, use_container_width=True)
 
    callout("WHY THIS MATTERS CLINICALLY",
            "Drug-metabolising genes (CYP2D6, CYP3A5, CYP2C19) carry variants "
            "with frequencies that differ substantially between Africans and "
            "Europeans. A standard dose calibrated in European trials can be "
            "too high or too low for a Nigerian patient. The ~43% diversity gap "
            "you see above is not an abstraction — it is the genetic basis "
            "for why pharmacogenomic algorithms must be validated locally.")
 
# ============================================================= TAB 4 — AIMS
with tab_aims:
    section_header(
        eyebrow="04 · The mechanism behind the clusters",
        title="A tiny fraction of variants does most of the work",
        lead="Of ~5,000 variants, only 20 have Fst above 0.3 — strongly "
             "differentiated between populations. The headline result: PCA "
             "using only the top-ranked AIMs recovers the same continental "
             "clusters as the full panel."
    )
 
    st.markdown(
        '<div style="font-family:\'Inter\'; color:#94A3B8; margin-bottom:1rem;">'
        'Adjust the number of top AIMs and watch the population structure '
        'rebuild itself in real time.</div>',
        unsafe_allow_html=True
    )
 
    n_top = st.select_slider(
        "Number of top AIMs by Fst",
        options=[10, 25, 50, 100, 200],
        value=50
    )
 
    selection = aims_pcas[str(n_top)]
    df_aims_plot = samples[['Sample', 'Population code',
                            'Superpopulation name', 'Population name']].copy()
    df_aims_plot['PC1'] = selection['pc1']
    df_aims_plot['PC2'] = selection['pc2']
 
    chart_aims = alt.Chart(df_aims_plot).mark_circle(size=50, opacity=0.75).encode(
        x=alt.X('PC1:Q', scale=alt.Scale(zero=False),
                title=f'PC1 — captures {selection["var_pc1"]:.1f}% of variance'),
        y=alt.Y('PC2:Q', scale=alt.Scale(zero=False),
                title=f'PC2 — captures {selection["var_pc2"]:.1f}% of variance'),
        color=alt.Color('Superpopulation name:N', scale=SUPERPOP_COLORS,
                        legend=alt.Legend(title="Ancestry", orient='right')),
        tooltip=['Sample:N', 'Population name:N', 'Superpopulation name:N']
    ).properties(height=520).interactive()
 
    st.altair_chart(chart_aims, use_container_width=True)
 
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class="kpi-card">
        <div class="kpi-value" style="font-size:2rem;">{selection['var_pc1']:.1f}%</div>
        <div class="kpi-label">PC1 variance</div>
        <div class="kpi-sub">vs {stats['pc1_full_var']:.1f}% in full panel</div>
        </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card">
        <div class="kpi-value" style="font-size:2rem;">{n_top}</div>
        <div class="kpi-label">Variants used</div>
        <div class="kpi-sub">{100*n_top/stats['n_variants']:.1f}% of full panel</div>
        </div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card">
        <div class="kpi-value" style="font-size:2rem;">
            {selection['var_pc1']+selection['var_pc2']:.1f}%</div>
        <div class="kpi-label">PC1 + PC2</div>
        <div class="kpi-sub">total variance captured</div>
        </div>""", unsafe_allow_html=True)
 
    callout("THIS IS HOW ANCESTRY TESTING WORKS",
            "Commercial ancestry inference panels don't sequence whole genomes — "
            "they read a few hundred carefully chosen variants exactly like these. "
            "By concentrating on the small subset of high-Fst markers, you "
            "throw away the within-population noise and amplify the between-"
            "population signal. The slider above lets you watch that effect "
            "in real time.")
 
# ============================================================= TAB 5 — METHOD
with tab_method:
    section_header(
        eyebrow="05 · Behind the scenes",
        title="How the analysis was built",
        lead="A transparent pipeline: from raw VCF to interactive app, "
             "all in Python on a laptop. Honest limitations included."
    )
 
    st.markdown("### Pipeline")
    pipeline = [
        ("01", "Parse chr22 VCF, sub-sample every 100th variant", "pysam"),
        ("02", "Build (1092 × 4943) genotype matrix, attach labels", "numpy / pandas"),
        ("03", "Global PCA & visualisation", "scikit-learn / Altair"),
        ("04", "t-SNE comparison", "scikit-learn"),
        ("05", "Within-European PCA replicating Novembre 2008", "scikit-learn"),
        ("06", "Within-Africa PCA across YRI / LWK / ASW", "scikit-learn"),
        ("07", "Out-of-Africa diversity quantification", "numpy"),
        ("08", "AIM identification via vectorised Fst calculation", "numpy"),
        ("09", "Top-50 AIMs PCA validation", "scikit-learn"),
        ("10", "Interactive deployment", "Streamlit"),
    ]
    for num, desc, tool in pipeline:
        st.markdown(f"""
        <div style="display:flex; align-items:center; padding:0.6rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.05);">
            <div style="font-family:'JetBrains Mono'; color:#D4600A;
                        width:40px; font-size:0.85rem;">{num}</div>
            <div style="flex:1; font-family:'Inter';">{desc}</div>
            <div style="font-family:'JetBrains Mono'; color:#94A3B8;
                        font-size:0.8rem;">{tool}</div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("### Limitations")
    limitations = [
        "Single chromosome — chr22 only, vs whole-genome Novembre 2008.",
        "Sub-sampling every 100th variant may have excluded some high-Fst markers.",
        "Phase 1 includes only 3 African populations; Phase 3 would give more.",
        "ASW samples are admixed and should not be read as continental African.",
        "Missing genotypes treated as homozygous reference — small reference bias.",
        "Fst calculated via simplified weighted-variance form, not Weir & Cockerham (1984).",
        "Method correlation between SNP-PCA distance and Fst is only r=0.344.",
        "No external validation of top AIMs against published panels."
    ]
    for lim in limitations:
        st.markdown(f"""
        <div style="display:flex; padding:0.4rem 0;">
            <div style="color:#D4600A; margin-right:0.75rem;">·</div>
            <div style="font-family:'Inter'; color:#94A3B8;">{lim}</div>
        </div>
        """, unsafe_allow_html=True)
 
    callout("FULL DOCUMENTATION",
            "All code, notebooks, references, and a comprehensive README live "
            "at <a style='color:#D4600A;' href='https://github.com/DrTim105/"
            "genes-and-geography'>github.com/DrTim105/genes-and-geography</a>.")
 
footer()








# streamlit_app/styles.py
"""All custom CSS lives here. Imported once by app.py via inject_css()."""
 
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
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        color: var(--text-secondary);
        max-width: 640px;
        margin: 1.5rem auto 0 auto;
        line-height: 1.5;
        font-weight: 300;
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