import streamlit as st

# ─────────────────────────────────────────────
# CONFIGURATION PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dar Khayam — Dashboard KPI",
    page_icon="🏨",
    layout="wide"
)

# ─────────────────────────────────────────────
# STYLE GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f2744;
    }
    [data-testid="stSidebar"] * {
        color: #e8f0fe !important;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0f2744 0%, #1a4a8a 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: white;
    }

    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        color: white !important;
    }

    .main-header p {
        margin: 0.3rem 0 0;
        color: #93b4d8;
    }

    /* Info banner */
    .info-banner {
        background-color: #e8f0fe;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 5px solid #1a4a8a;
        margin-bottom: 20px;
        font-size: 14px;
    }

    /* KPI cards */
    [data-testid="metric-container"] {
        background: #f8fafd;
        border: 1px solid #e2eaf4;
        border-radius: 10px;
        padding: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏨 Hôtel Dar Khayam</h1>
    <p>Dashboard KPI — Analyse des performances globales de l’hôtel</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INFO (EN HAUT DE PAGE comme demandé)
# ─────────────────────────────────────────────
st.markdown("""
<div class="info-banner">
👉 Utilise le menu à gauche pour explorer les départements : Hébergement, Restauration, RH et Énergie
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI GLOBAUX (SIMULÉS / EXEMPLE)
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Chiffre d'affaires", "1 250 000 TND")
col2.metric("🛏️ Taux d’occupation", "78 %")
col3.metric("👥 Masse salariale", "420 000 TND")
col4.metric("⚡ Coût énergie", "120 000 TND")

st.markdown("---")

# ─────────────────────────────────────────────
# CARDS DÉPARTEMENTS
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("🛏️ Hébergement\n\nRevPAR, ADR, occupation, nuitées")

with c2:
    st.info("🍽️ Restauration\n\nFood cost, marge brute, CA F&B")

with c3:
    st.info("👥 Ressources Humaines\n\nProductivité, masse salariale")

with c4:
    st.info("⚡ Énergie\n\nÉlectricité, eau, gaz, coûts STEG/SONEDE")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Projet PFE — Dashboard Intelligent Hôtelier | Dar Khayam | 2025")
