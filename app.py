import streamlit as st
import mysql.connector

# ─────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dar Khayam — Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ─────────────────────────────────────────────
# CONNEXION MYSQL
# ─────────────────────────────────────────────
try:
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"]),
        connection_timeout=10,
        ssl_disabled=True
    )
    cursor = conn.cursor()

except Exception as e:
    st.error(f"Erreur MySQL ❌ : {e}")
    st.stop()

# ─────────────────────────────────────────────
# CSS GLOBAL (VERSION PRO)
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* BODY */
body {
    background-color: #f5f7fb;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #9ca3af !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
}

/* HEADER */
.main-header {
    background: linear-gradient(135deg, #0D47A1, #1976D2);
    padding: 1.8rem 2rem;
    border-radius: 14px;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}

.main-header h1 {
    margin: 0;
    font-size: 1.9rem;
    color: white !important;
}

.main-header p {
    margin-top: 0.3rem;
    color: #dbeafe;
}

/* KPI */
[data-testid="metric-container"] {
    background: white;
    border-radius: 14px;
    padding: 18px !important;
    border-top: 4px solid #E65100;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transition: 0.2s ease-in-out;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
}

/* INFO BOX */
div[data-testid="stInfo"] {
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

/* PAGE SPACING */
div.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER (HOME)
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏨 Hôtel Dar Khayam</h1>
    <p>Dashboard intelligent de performance hôtelière — Analyse KPI en temps réel</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI DASHBOARD
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🛏️ Occupation", "78%", "↑ 3%")

with col2:
    st.metric("💰 RevPAR", "142 TND", "↑ 5 TND")

with col3:
    st.metric("🍽️ CA F&B", "32K TND", "↓ 2%")

with col4:
    st.metric("⚡ Énergie", "8.4K TND", "↑ 1.2%")

st.markdown("---")

# ─────────────────────────────────────────────
# MODULES DASHBOARD
# ─────────────────────────────────────────────
st.markdown("### 📊 Modules du système")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background:white;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #0D47A1;
        box-shadow:0 3px 10px rgba(0,0,0,0.05);
    ">
    🛏️ <b>Hébergement</b><br>
    Occupation • ADR • RevPAR • Nuitées
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background:white;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #E65100;
        box-shadow:0 3px 10px rgba(0,0,0,0.05);
    ">
    🍽️ <b>Restauration</b><br>
    CA F&B • Food Cost • Marges
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background:white;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #1B5E20;
        box-shadow:0 3px 10px rgba(0,0,0,0.05);
    ">
    ⚡ <b>Énergie</b><br>
    Électricité • Eau • Gaz • STEG
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.caption("Projet de Fin d'Études — Dashboard KPI Informatisé | Hôtel Dar Khayam | 2024-2025")

