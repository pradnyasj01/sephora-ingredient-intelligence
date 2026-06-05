import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px
import numpy as np
import re
from collections import Counter
from html import escape
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Ingredient Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif !important;
    background-color: #f7f4ef;
    color: #1a1410;
}
.stApp { background: #f7f4ef; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 4rem 6rem 4rem; max-width: 1200px; }

/* Multiselect override */
div[data-baseweb="select"] > div {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #c8b89a !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0.3rem 0 !important;
}
span[data-baseweb="tag"] {
    background: #1a1410 !important;
    color: #f7f4ef !important;
    border-radius: 0 !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    font-family: 'Jost', sans-serif !important;
}
span[data-baseweb="tag"] span { color: #f7f4ef !important; }
div[data-baseweb="select"] input { color: #1a1410 !important; }
div[data-baseweb="select"] div {
    color: #1a1410 !important;
}
div[data-baseweb="select"] [class*="singleValue"] {
    color: #1a1410 !important;
}
div[data-baseweb="select"] [class*="placeholder"] {
    color: #9a8a78 !important;
}
div[data-baseweb="select"] > div {
    min-height: 56px !important;
    align-items: center !important;
    overflow: visible !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
div[data-baseweb="select"] input {
    line-height: 24px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
div[data-baseweb="select"] [class*="placeholder"],
div[data-baseweb="select"] [class*="singleValue"],
div[data-baseweb="select"] [class*="valueContainer"] {
    line-height: 24px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    display: flex !important;
    align-items: center !important;
}
.stTextInput input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #c8b89a !important;
    border-radius: 0 !important;
    color: #1a1410 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.95rem !important;
    min-height: 48px !important;
}

/* Selectbox */
div[data-baseweb="select"] svg { color: #c8b89a !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #f7f4ef; }
::-webkit-scrollbar-thumb { background: #c8b89a; }

/* Navbar */
.navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 2rem 0 1.5rem; border-bottom: 1px solid #1a1410;
    margin-bottom: 4rem;
}
.nav-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem; font-weight: 400; letter-spacing: 4px;
    text-transform: uppercase; color: #1a1410;
}
.nav-right { font-size: 0.65rem; color: #9a8a78; letter-spacing: 2px; text-transform: uppercase; }

/* Hero */
.hero { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; margin-bottom: 5rem; align-items: end; }
.hero-left {}
.hero-eyebrow { font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #9a8a78; margin-bottom: 1.5rem; }
.hero-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 5rem; font-weight: 300; color: #1a1410;
    line-height: 1.0; letter-spacing: -1px;
}
.hero-title em { font-style: italic; color: #8a6a4a; }
.hero-right { padding-bottom: 0.5rem; }
.hero-desc { font-size: 0.9rem; color: #6a5a48; line-height: 1.9; font-weight: 300; border-left: 1px solid #c8b89a; padding-left: 1.5rem; }

/* Stat strip */
.stat-strip { display: grid; grid-template-columns: repeat(4,1fr); border-top: 1px solid #1a1410; border-bottom: 1px solid #1a1410; margin-bottom: 5rem; }
.stat-cell { padding: 2rem 1rem; border-right: 1px solid #e8dfd4; }
.stat-cell:last-child { border-right: none; }
.stat-num { font-family: 'Cormorant Garamond', serif; font-size: 3rem; font-weight: 300; color: #1a1410; line-height: 1; }
.stat-label { font-size: 0.62rem; color: #9a8a78; letter-spacing: 2px; margin-top: 0.5rem; text-transform: uppercase; }

/* Section */
.sec-wrap { margin-bottom: 5rem; }
.sec-top { display: flex; align-items: baseline; gap: 2rem; margin-bottom: 2rem; border-bottom: 1px solid #e8dfd4; padding-bottom: 1rem; }
.sec-num { font-size: 0.6rem; color: #c8b89a; letter-spacing: 2px; }
.sec-title { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 300; color: #1a1410; }
.sec-desc { font-size: 0.78rem; color: #9a8a78; letter-spacing: 0.5px; margin-left: auto; max-width: 280px; text-align: right; line-height: 1.6; }

/* Filter label */
.filter-label { font-size: 0.62rem; color: #9a8a78; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.5rem; }

/* Side cards */
.side-card { border: 1px solid #e8dfd4; padding: 1.5rem; margin-bottom: 1rem; }
.sc-label { font-size: 0.6rem; color: #9a8a78; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.8rem; }
.sc-name { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: #1a1410; margin-bottom: 0.3rem; }
.sc-num { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 300; color: #8a6a4a; line-height: 1; }
.sc-sub { font-size: 0.7rem; color: #9a8a78; margin-top: 0.2rem; }

/* Brand card */
.brand-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 1px solid #e8dfd4; margin-bottom: 1rem; }
.bs-cell { padding: 1.2rem 1.4rem; border-right: 1px solid #e8dfd4; border-bottom: 1px solid #e8dfd4; }
.bs-cell:nth-child(2), .bs-cell:nth-child(4) { border-right: none; }
.bs-cell:nth-child(3), .bs-cell:nth-child(4) { border-bottom: none; }
.bs-num { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: #1a1410; }
.bs-label { font-size: 0.6rem; color: #9a8a78; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 0.2rem; }

/* Product list */
.prod-list { border: 1px solid #e8dfd4; }
.prod-header { padding: 0.8rem 1.2rem; border-bottom: 1px solid #e8dfd4; font-size: 0.6rem; color: #9a8a78; letter-spacing: 2px; text-transform: uppercase; background: #f0ebe3; }
.prod-row { display: flex; align-items: center; justify-content: space-between; padding: 0.9rem 1.2rem; border-bottom: 1px solid #f0ebe3; }
.prod-row:last-child { border-bottom: none; }
.prod-name { font-size: 0.82rem; color: #1a1410; font-weight: 400; }
.prod-surf { font-size: 0.65rem; color: #9a8a78; margin-top: 0.15rem; letter-spacing: 0.5px; }
.prod-mild { color: #5a8a5a; }
.prod-trad { color: #8a4a4a; }
.prod-right { text-align: right; }
.prod-rating { font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: #1a1410; }
.prod-price { font-size: 0.7rem; color: #9a8a78; margin-top: 0.1rem; }

/* NLP review intelligence */
.nlp-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 0; border: 1px solid #e8dfd4; margin-bottom: 1.5rem; }
.nlp-cell { padding: 1.2rem 1.4rem; border-right: 1px solid #e8dfd4; }
.nlp-cell:last-child { border-right: none; }
.nlp-num { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 300; color: #1a1410; line-height: 1; }
.nlp-label { font-size: 0.6rem; color: #9a8a78; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 0.3rem; }
.chip-wrap { display: flex; flex-wrap: wrap; gap: 0.45rem; margin: 0.8rem 0 1.5rem; }
.term-chip { border: 1px solid #d8cab8; padding: 0.35rem 0.55rem; font-size: 0.68rem; color: #6a5a48; letter-spacing: 0.5px; background: #fbf8f3; }
.review-card { border-left: 1px solid #c8b89a; padding: 0.9rem 1rem; margin-bottom: 0.8rem; background: #fbf8f3; }
.review-meta { font-size: 0.6rem; color: #9a8a78; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.4rem; }
.review-text { font-size: 0.82rem; color: #6a5a48; line-height: 1.65; font-weight: 300; }

/* Insight grid */
.insight-grid { display: grid; grid-template-columns: repeat(2,1fr); border: 1px solid #e8dfd4; margin-top: 5rem; }
.ic { padding: 2.5rem; border-right: 1px solid #e8dfd4; border-bottom: 1px solid #e8dfd4; }
.ic:nth-child(2), .ic:nth-child(4) { border-right: none; }
.ic:nth-child(3), .ic:nth-child(4) { border-bottom: none; }
.ic-n { font-family: 'Cormorant Garamond', serif; font-size: 4rem; font-weight: 300; color: #e8dfd4; line-height: 1; margin-bottom: 0.8rem; }
.ic-h { font-size: 0.78rem; color: #8a6a4a; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.8rem; font-weight: 500; }
.ic-b { font-size: 1rem; color: #6a5a48; line-height: 1.7; font-weight: 300; }

.footer { text-align: center; padding: 4rem 0 1rem; font-size: 0.6rem; color: #c8b89a; letter-spacing: 3px; text-transform: uppercase; border-top: 1px solid #e8dfd4; margin-top: 4rem; }

/* Scroll reveal */
@keyframes reveal-up {
    from { opacity: 0; transform: translateY(34px); filter: blur(8px); }
    to { opacity: 1; transform: translateY(0); filter: blur(0); }
}

@supports (animation-timeline: view()) {
    .hero,
    .stat-strip,
    .sec-top,
    .stPlotlyChart,
    .side-card,
    .brand-stats,
    .prod-list,
    .nlp-grid,
    .review-card,
    .insight-grid,
    .footer {
        opacity: 0;
        animation: reveal-up 0.85s cubic-bezier(.22, 1, .36, 1) both;
        animation-timeline: view();
        animation-range: entry 0% cover 28%;
    }

    .side-card:nth-child(2),
    .review-card:nth-child(2) {
        animation-range: entry 8% cover 34%;
    }
}

</style>
""", unsafe_allow_html=True)

mpl.rcParams.update({
    'figure.facecolor': '#f7f4ef', 'axes.facecolor': '#f7f4ef',
    'axes.edgecolor': '#e8dfd4', 'axes.labelcolor': '#9a8a78',
    'xtick.color': '#9a8a78', 'ytick.color': '#9a8a78',
    'text.color': '#1a1410', 'grid.color': '#e8dfd4',
    'grid.linewidth': 0.5, 'font.family': 'sans-serif',
})

@st.cache_data
def load_data():
    products = pd.read_csv("product_info.csv")

    sample_path = "reviews_sample.csv"
    if Path(sample_path).exists():
        reviews = pd.read_csv(sample_path)
    else:
        reviews = pd.concat([
            pd.read_csv("reviews_0-250.csv"),
            pd.read_csv("reviews_250-500.csv"),
            pd.read_csv("reviews_500-750.csv"),
            pd.read_csv("reviews_750-1250.csv"),
            pd.read_csv("reviews_1250-end.csv")
        ], ignore_index=True)

    return products, reviews

products, reviews = load_data()
FULL_REVIEW_COUNT = 1_094_411

MILD = ['cocamidopropyl betaine','coco-glucoside','decyl glucoside',
        'sodium cocoyl isethionate','lauryl glucoside','disodium laureth sulfosuccinate']
HARSH = ['sodium lauryl sulfate','sls','sodium laureth sulfate','sles',
         'ammonium lauryl sulfate','ammonium laureth sulfate']
ALL_SURF = HARSH + MILD
SURFACTANT_LABELS = {
    'cocamidopropyl betaine': 'Cocamidopropyl Betaine',
    'coco-glucoside': 'Coco-Glucoside',
    'decyl glucoside': 'Decyl Glucoside',
    'sodium cocoyl isethionate': 'Sodium Cocoyl Isethionate',
    'lauryl glucoside': 'Lauryl Glucoside',
    'disodium laureth sulfosuccinate': 'Disodium Laureth Sulfosuccinate',
    'sodium lauryl sulfate': 'Sodium Lauryl Sulfate',
    'sls': 'SLS',
    'sodium laureth sulfate': 'Sodium Laureth Sulfate',
    'sles': 'SLES',
    'ammonium lauryl sulfate': 'Ammonium Lauryl Sulfate',
    'ammonium laureth sulfate': 'Ammonium Laureth Sulfate',
}

def classify(ing):
    if pd.isna(ing): return 'Unknown'
    ing = ing.lower()
    if any(h in ing for h in HARSH): return 'Traditional'
    if any(m in ing for m in MILD): return 'Mild / Green'
    return 'Unknown'

products['surfactant_type'] = products['ingredients'].apply(classify)
products['ingredients_lower'] = products['ingredients'].fillna('').str.lower()

mild_count = (products['surfactant_type'] == 'Mild / Green').sum()
trad_count = (products['surfactant_type'] == 'Traditional').sum()

THEME_PATTERNS = {
    'Gentle / Non-Stripping': ['gentle', 'non stripping', 'non-stripping', 'soft', 'calm', 'sensitive'],
    'Hydration': ['hydrating', 'hydrated', 'moisture', 'moisturizing', 'dryness', 'dewy'],
    'Irritation': ['irritated', 'irritation', 'burning', 'stinging', 'redness', 'itchy'],
    'Breakouts': ['breakout', 'breakouts', 'acne', 'pimples', 'clogged', 'comedogenic'],
    'Scent / Fragrance': ['scent', 'smell', 'fragrance', 'perfume', 'fragranced'],
    'Texture / Feel': ['texture', 'creamy', 'foamy', 'lather', 'sticky', 'greasy'],
    'Cleansing Power': ['cleanse', 'cleansed', 'makeup', 'oil', 'residue', 'double cleanse'],
    'Value / Price': ['price', 'expensive', 'worth', 'value', 'repurchase', 'cost'],
}

STOPWORDS = {
    'about', 'after', 'again', 'also', 'because', 'been', 'being', 'bought',
    'could', 'does', 'even', 'from', 'have', 'just', 'like', 'love', 'make',
    'more', 'much', 'only', 'product', 'really', 'skin', 'still', 'than',
    'that', 'this', 'using', 'very', 'with', 'would', 'when', 'will', 'your'
}

@st.cache_data
def review_intelligence(reviews_df, product_id):
    subset = reviews_df[reviews_df['product_id'] == product_id].copy()
    subset['review_text'] = subset['review_text'].fillna('').astype(str)
    subset = subset[subset['review_text'].str.len() > 20]

    if subset.empty:
        return subset, pd.Series(dtype=int), [], 0, 0, 0

    text_blob = ' '.join(subset['review_text'].str.lower().tolist())
    theme_counts = {}
    for theme, patterns in THEME_PATTERNS.items():
        theme_counts[theme] = sum(text_blob.count(pattern) for pattern in patterns)

    words = re.findall(r"[a-z][a-z'-]{3,}", text_blob)
    terms = [
        word.strip("'")
        for word in words
        if word not in STOPWORDS and len(word.strip("'")) > 3
    ]
    top_terms = [term for term, _ in Counter(terms).most_common(14)]

    positive_share = (subset['rating'] >= 4).mean() * 100
    critical_share = (subset['rating'] <= 2).mean() * 100
    recommended_share = subset['is_recommended'].mean() * 100 if 'is_recommended' in subset else 0

    return subset, pd.Series(theme_counts).sort_values(ascending=True), top_terms, positive_share, critical_share, recommended_share

def render_review_cards(df, label, limit=2):
    cards = ''
    for _, row in df.head(limit).iterrows():
        text = escape(str(row.get('review_text', ''))[:360])
        rating = row.get('rating', 0)
        title = escape(str(row.get('review_title', 'Review')))
        cards += f"""
        <div class="review-card">
            <div class="review-meta">{label} · {rating:.0f} stars · {title[:60]}</div>
            <div class="review-text">{text}</div>
        </div>
        """
    return cards or '<div class="review-text">No matching reviews found for this product.</div>'

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Ingredient Intelligence</div>
    <div class="nav-right">Personal Care · Surfactant Analysis · Sephora Dataset</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-left">
        <div class="hero-eyebrow">Formulation Intelligence</div>
        <div class="hero-title">What's<br>inside your<br><em>beauty routine?</em></div>
    </div>
    <div class="hero-right">
        <div class="hero-desc">
            A data-driven analysis of surfactant trends across {len(products):,} Sephora 
            products and {FULL_REVIEW_COUNT/1_000_000:.1f}M dataset reviews — revealing 
            the decisive shift from traditional sulfates to green chemistry alternatives 
            in premium personal care.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stat strip ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-strip">
    <div class="stat-cell">
        <div class="stat-num">{len(products):,}</div>
        <div class="stat-label">Products Analyzed</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">{FULL_REVIEW_COUNT/1_000_000:.1f}M</div>
        <div class="stat-label">Dataset Reviews</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">{mild_count}</div>
        <div class="stat-label">Mild Surfactant Products</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">{trad_count}</div>
        <div class="stat-label">Traditional Products</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-top">
    <div class="sec-num">01</div>
    <div class="sec-title">Surfactant Frequency</div>
    <div class="sec-desc">Filter by category to reveal formulation differences across product segments</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="filter-label">Filter by Category</div>', unsafe_allow_html=True)
categories = sorted(products['primary_category'].dropna().unique().tolist())
selected_cats = st.multiselect("", categories, default=[], placeholder="All categories", label_visibility="collapsed")

filtered = products[products['primary_category'].isin(selected_cats)] if selected_cats else products

surf_results = {}
for s in ALL_SURF:
    surf_results[s] = filtered['ingredients_lower'].str.contains(s, na=False).sum()
surf_counts = pd.Series(surf_results).sort_values(ascending=True)

col1, col2 = st.columns([3, 1])
with col1:
    surf_df = surf_counts.reset_index()
    surf_df.columns = ['surfactant', 'count']
    surf_df['surfactant_label'] = surf_df['surfactant'].map(SURFACTANT_LABELS)
    surf_df['type'] = np.where(
        surf_df['surfactant'].isin(MILD),
        'Mild / Green',
        'Traditional'
    )

    fig1 = px.bar(
        surf_df,
        x='count',
        y='surfactant_label',
        color='type',
        orientation='h',
        text='count',
        color_discrete_map={
            'Mild / Green': '#5a8a5a',
            'Traditional': '#8a4a4a'
        },
        labels={'count': 'Number of Products', 'surfactant_label': ''}
    )

    fig1.update_traces(
        textposition='outside',
        textfont=dict(color='#6a5a48', size=13),
        marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>%{x} products<extra></extra>'
    )

    fig1.update_layout(
        height=560,
        plot_bgcolor='#f7f4ef',
        paper_bgcolor='#f7f4ef',
        font=dict(color='#1a1410', family='Jost', size=13),
        showlegend=False,
        xaxis=dict(
            title=dict(text='Number of Products', font=dict(color='#6a5a48', size=13)),
            gridcolor='#eee7dc',
            zeroline=False,
            tickfont=dict(color='#6a5a48', size=13)
        ),
        yaxis=dict(
            categoryorder='total ascending',
            tickfont=dict(color='#6a5a48', size=13)
        ),
        margin=dict(l=230, r=40, t=10, b=45)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={'displayModeBar': False}
    )

    st.markdown(
        '<p style="font-size:0.78rem;color:#6a5a48;letter-spacing:1px;">'
        '<span style="color:#5a8a5a;">■</span> Mild / green surfactants &nbsp;&nbsp; '
        '<span style="color:#8a4a4a;">■</span> Traditional sulfates</p>',
        unsafe_allow_html=True
    )
with col2:
    top_mild_name = surf_counts[surf_counts.index.isin(MILD)].index[-1]
    top_mild_val = int(surf_counts[surf_counts.index.isin(MILD)].iloc[-1])
    sls_val = int(surf_counts.get('sodium lauryl sulfate', 0))
    st.markdown(f"""
    <div class="side-card">
        <div class="sc-label">Top Mild Surfactant</div>
        <div class="sc-name">{SURFACTANT_LABELS.get(top_mild_name, top_mild_name.title())}</div>
        <div class="sc-num">{top_mild_val}</div>
        <div class="sc-sub">products in selection</div>
    </div>
    <div class="side-card">
        <div class="sc-label">SLS Presence</div>
        <div class="sc-num" style="color:#8a4a4a;">{sls_val}</div>
        <div class="sc-sub">products containing SLS</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-top" style="margin-top:4rem;">
    <div class="sec-num">02</div>
    <div class="sec-title">Brand Explorer</div>
    <div class="sec-desc">Search any brand to reveal their surfactant profile and top-rated products</div>
</div>
""", unsafe_allow_html=True)

all_brands = sorted(products['brand_name'].dropna().unique().tolist())
selected_brand = st.selectbox(
    "",
    all_brands,
    index=None,
    placeholder="Search or select a brand",
    label_visibility="collapsed"
)
brand_products = pd.DataFrame()

if selected_brand:
    brand_products = products[products['brand_name'] == selected_brand].copy()
    b_mild = (brand_products['surfactant_type'] == 'Mild / Green').sum()
    b_trad = (brand_products['surfactant_type'] == 'Traditional').sum()
    b_avg_rating = brand_products['rating'].mean() if 'rating' in brand_products.columns else 0
    b_avg_price = brand_products['price_usd'].mean() if 'price_usd' in brand_products.columns else 0

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class="brand-stats">
            <div class="bs-cell">
                <div class="bs-num" style="color:#5a8a5a;">{b_mild}</div>
                <div class="bs-label">Mild Products</div>
            </div>
            <div class="bs-cell">
                <div class="bs-num" style="color:#8a4a4a;">{b_trad}</div>
                <div class="bs-label">Traditional</div>
            </div>
            <div class="bs-cell">
                <div class="bs-num">{b_avg_rating:.2f}</div>
                <div class="bs-label">Avg Rating</div>
            </div>
            <div class="bs-cell">
                <div class="bs-num">${b_avg_price:.0f}</div>
                <div class="bs-label">Avg Price</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        top_products = (brand_products
            .sort_values('rating', ascending=False)
            .head(6))

        st.markdown(f"""
        <div class="prod-list">
            <div class="prod-header">Top Rated Products — {selected_brand}</div>
        </div>
        """, unsafe_allow_html=True)
        
        for _, row in top_products.iterrows():
            surf = row['surfactant_type']
            sc = 'prod-mild' if surf == 'Mild / Green' else 'prod-trad' if surf == 'Traditional' else ''
            rating_val = f"{row['rating']:.2f} ★" if pd.notna(row.get('rating')) else '—'
            price_val = f"${row['price_usd']:.0f}" if pd.notna(row.get('price_usd')) else ''
            name = str(row.get('product_name',''))[:48]
            detail = row.get('secondary_category', surf) if surf == 'Unknown' else surf
            st.markdown(f"""
            <div class="prod-row">
                <div>
                    <div class="prod-name">{name}</div>
                    <div class="prod-surf {sc}">{detail}</div>
                </div>
                <div class="prod-right">
                    <div class="prod-rating">{rating_val}</div>
                    <div class="prod-price">{price_val}</div>
                </div>
            </div>""", unsafe_allow_html=True)
else:
    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-top" style="margin-top:4rem;">
    <div class="sec-num">03</div>
    <div class="sec-title">Review Intelligence</div>
    <div class="sec-desc">Lightweight NLP signals from customer language, not just star ratings</div>
</div>
""", unsafe_allow_html=True)

brand_review_products = pd.DataFrame()
if selected_brand:
    brand_review_products = (brand_products
        .merge(reviews.groupby('product_id').agg(review_count=('rating', 'size'), avg_review_rating=('rating', 'mean')).reset_index(),
               on='product_id', how='left')
        .dropna(subset=['review_count'])
        .sort_values('review_count', ascending=False))

if not selected_brand:
    st.markdown("""
    <div class="side-card" style="background:#fbf8f3;">
        <div class="sc-label">Review Intelligence</div>
        <div class="sc-name">Select a brand above to analyze reviews</div>
        <div class="sc-sub">This section mines customer review text for product-level themes once the selected brand has matching review rows.</div>
    </div>
    """, unsafe_allow_html=True)
elif brand_review_products.empty:
    st.markdown("""
    <div class="side-card" style="background:#fbf8f3;">
        <div class="sc-label">Review Text Coverage</div>
        <div class="sc-name">Detailed reviews are not included for this brand</div>
        <div class="sc-sub">The product catalog still provides brand-level ratings and review counts above, but the Kaggle review-text files do not contain matching rows for this brand's product IDs.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    product_options = {
        f"{row.product_name} ({int(row.review_count):,} reviews)": row.product_id
        for row in brand_review_products.itertuples()
    }
    selected_product_label = st.selectbox(
        "",
        list(product_options.keys()),
        label_visibility="collapsed"
    )
    selected_product_id = product_options[selected_product_label]
    selected_product = brand_review_products[brand_review_products['product_id'] == selected_product_id].iloc[0]

    product_reviews, theme_counts, top_terms, positive_share, critical_share, recommended_share = review_intelligence(reviews, selected_product_id)
    review_count = len(product_reviews)

    st.markdown(f"""
    <div class="nlp-grid">
        <div class="nlp-cell">
            <div class="nlp-num">{review_count:,}</div>
            <div class="nlp-label">Text Reviews Mined</div>
        </div>
        <div class="nlp-cell">
            <div class="nlp-num">{positive_share:.0f}%</div>
            <div class="nlp-label">4-5 Star Share</div>
        </div>
        <div class="nlp-cell">
            <div class="nlp-num">{recommended_share:.0f}%</div>
            <div class="nlp-label">Recommendation Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.15, 1])
    with col1:
        fig4, ax4 = plt.subplots(figsize=(7.5, 4.3))
        colors = ['#8a6a4a' if val == theme_counts.max() else '#c8b89a' for val in theme_counts.values]
        ax4.barh(theme_counts.index, theme_counts.values, color=colors, height=0.55, zorder=3)
        ax4.set_xlabel("Keyword Mentions", fontsize=8)
        ax4.grid(axis='x', alpha=0.35, zorder=0)
        ax4.spines[['top','right','left','bottom']].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig4)

    with col2:
        chips = ''.join(f'<span class="term-chip">{escape(term)}</span>' for term in top_terms)
        st.markdown(f"""
        <div class="side-card">
            <div class="sc-label">Selected Product</div>
            <div class="sc-name">{escape(str(selected_product['product_name']))}</div>
            <div class="sc-sub">{escape(str(selected_brand))} · {escape(str(selected_product['surfactant_type']))} · ${selected_product['price_usd']:.0f}</div>
        </div>
        <div class="filter-label">Most Frequent Review Terms</div>
        <div class="chip-wrap">{chips}</div>
        <div class="side-card">
            <div class="sc-label">Critical Review Share</div>
            <div class="sc-num" style="color:#8a4a4a;">{critical_share:.0f}%</div>
            <div class="sc-sub">1-2 star reviews among mined text reviews</div>
        </div>
        """, unsafe_allow_html=True)

    positive_examples = product_reviews[product_reviews['rating'] >= 4].sort_values('helpfulness', ascending=False)
    critical_examples = product_reviews[product_reviews['rating'] <= 2].sort_values('helpfulness', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="filter-label">High-Rating Review Signals</div>', unsafe_allow_html=True)
        st.markdown(render_review_cards(positive_examples, 'Positive signal'), unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="filter-label">Critical Review Signals</div>', unsafe_allow_html=True)
        st.markdown(render_review_cards(critical_examples, 'Critical signal'), unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-top" style="margin-top:4rem;">
    <div class="sec-num">04</div>
    <div class="sec-title">Price vs. Formulation</div>
    <div class="sec-desc">Do premium products invest in greener surfactant chemistry?</div>
</div>
""", unsafe_allow_html=True)

price_data = products[products['surfactant_type'].isin(['Mild / Green','Traditional'])].copy()
price_data = price_data[price_data['price_usd'].notna() & (price_data['price_usd']>0) & (price_data['price_usd']<300)]

fig3 = px.scatter(
    price_data,
    x='price_usd',
    y='rating',
    color='surfactant_type',
    hover_data=['brand_name', 'product_name', 'primary_category'],
    color_discrete_map={
        'Mild / Green': '#5a8a5a',
        'Traditional': '#8a4a4a'
    },
    labels={
        'price_usd': 'Price (USD)',
        'rating': 'Product Rating',
        'surfactant_type': ''
    }
)

fig3.update_traces(marker=dict(size=8, opacity=0.55))
fig3.update_layout(
    height=520,
    plot_bgcolor='#f7f4ef',
    paper_bgcolor='#f7f4ef',
    font=dict(color='#1a1410', family='Jost', size=13),
    xaxis=dict(
        title=dict(text='Price (USD)', font=dict(color='#6a5a48', size=13)),
        gridcolor='#eee7dc',
        zeroline=False,
        tickfont=dict(color='#6a5a48', size=13)
    ),
    yaxis=dict(
        title=dict(text='Product Rating', font=dict(color='#6a5a48', size=13)),
        gridcolor='#eee7dc',
        tickfont=dict(color='#6a5a48', size=13)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(color='#6a5a48', size=12)
    ),
    margin=dict(l=20, r=20, t=40, b=45)
)

st.plotly_chart(
    fig3,
    use_container_width=True,
    config={'displayModeBar': False}
)
# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="insight-grid">
    <div class="ic">
        <div class="ic-n">01</div>
        <div class="ic-h">What The Catalog Actually Shows</div>
        <div class="ic-b">Across 8,494 Sephora products, mild surfactants appear far more often than traditional sulfate systems. This supports a measurable premium-market shift toward gentler cleansing chemistry.</div>
    </div>
    <div class="ic">
        <div class="ic-n">02</div>
        <div class="ic-h">Cocamidopropyl Betaine Leads</div>
        <div class="ic-b">The top detected surfactant is cocamidopropyl betaine, a common amphoteric ingredient used to improve mildness and foam quality. That makes the finding chemically interpretable, not just a frequency count.</div>
    </div>
    <div class="ic">
        <div class="ic-n">03</div>
        <div class="ic-h">Reviews Add Context</div>
        <div class="ic-b">The Review Intelligence section connects star ratings to customer language, surfacing themes like hydration, irritation, scent, texture, and cleansing power for the selected brand and product.</div>
    </div>
    <div class="ic">
        <div class="ic-n">04</div>
        <div class="ic-h">Business Use Case</div>
        <div class="ic-b">A personal-care team could use this workflow to benchmark brands, identify ingredient-positioning opportunities, and connect formulation choices with customer perception before launching or reformulating a cleanser.</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<script>
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.stat-cell, .sec-top, .side-card, .ic, .prod-row, .bs-cell').forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
});
</script>
""", unsafe_allow_html=True)
st.markdown('<div class="footer">Ingredient Intelligence &nbsp;·&nbsp; Sephora Dataset &nbsp;·&nbsp; 8,494 Products &nbsp;·&nbsp; 1.09M Reviews</div>', unsafe_allow_html=True)