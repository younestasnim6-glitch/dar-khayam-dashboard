import streamlit as st
import mysql.connector

# ── CONFIG ─────────────────────────────
st.set_page_config(
    page_title="Dar Khayam — Dashboard KPI",
    page_icon="🏨",
    layout="wide"
)

# ── CONNEXION MYSQL ────────────────────
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=int(st.secrets["mysql"]["port"]),
            connection_timeout=10
        )
        return conn
    except Exception as e:
        st.error(f"Erreur MySQL ❌ : {e}")
        st.stop()

conn = get_connection()
cursor = conn.cursor()

# ── CSS (version TOPBAR + DESIGN PRO) ─────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f7f9fc; }

    [data-testid="stSidebar"] { display: none !important; }

    .topbar {
        background: white;
        border-bottom: 2px solid #e8f0fe;
        padding: 0.75rem 2rem;
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .topbar-logo {
        font-weight: 800;
        color: #E65100;
    }

    .nav-link {
        padding: 6px 14px;
        border-radius: 20px;
        background: #fff3e0;
        color: #E65100 !important;
        text-decoration: none;
    }

    .hero {
        background: linear-gradient(135deg, #1565C0, #E65100);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-top: 1rem;
    }

    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e8f0fe;
    }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ─────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">🏨 DAR KHAYAM</div>
    <a class="nav-link" href="/1_Hebergement">Hébergement</a>
    <a class="nav-link" href="/2_Restauration">Restauration</a>
    <a class="nav-link" href="/3_RH">RH</a>
    <a class="nav-link" href="/4_Energie">Énergie</a>
</div>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Tableau de bord KPI</h1>
    <p>Hôtel Dar Khayam — Hammamet Nord</p>
</div>
""", unsafe_allow_html=True)

# ── KPI EXEMPLE (tu peux remplacer par MySQL plus tard)
c1, c2, c3 = st.columns(3)

c1.metric("💰 CA Total", "8 935 578 DT")
c2.metric("🛏️ Nuitées", "55 933")
c3.metric("📊 Occupation", "54.2 %")

st.markdown("---")
st.caption("PFE Dashboard - Dar Khayam")
           
           

