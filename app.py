import streamlit as st
import mysql.connector

st.set_page_config(
    page_title="Dar Khayam — Dashboard",
    page_icon="🏨",
    layout="wide"
)

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
    
# ── CSS global partagé ──────────────────────────────────────────────
st.markdown("""
<style>

/* ================= SIDEBAR ================= */
[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Labels sidebar */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #9ca3af !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
}

/* ================= HEADER ================= */
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

/* ================= KPI CARDS ================= */
[data-testid="metric-container"] {
    background: white;
    border-radius: 14px;
    padding: 18px !important;
    border-top: 4px solid #E65100;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transition: 0.2s ease-in-out;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
}

/* ================= INFO BOXES ================= */
div[data-testid="stInfo"] {
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

/* ================= GLOBAL ================= */
body {
    background-color: #f5f7fb;
}

</style>
""", unsafe_allow_html=True)

# ── Page d'accueil ───────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏨 Hôtel Dar Khayam</h1>
    <p>Tableau de bord KPI — Sélectionnez un département dans la barre de navigation à gauche</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("🛏️ **Hébergement**\n\nTaux d'occupation • ADR • RevPAR • Nuitées")
with col2:
    st.info("🍽️ **Restauration**\n\nFood cost, marge brute, CA F&B")
with col3:
    st.info("👥 **Ressources Humaines**\n\nMasse salariale, productivité, saisonnalité")
with col4:
    st.info("📈 **Chiffre d'affaires**\n\nCA global, évolution, analyse mensuelle")
with col5:
    st.info("⚡ **Énergie**\n\nÉlectricité, eau, gaz, coûts STEG/SONEDE")

st.markdown("""
<style>
div.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)
st.caption("Projet de Fin d'Études — Dashboard KPI Informatisé | Hôtel Dar Khayam | 2024-2025")
           

