import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
 
st.set_page_config(page_title="Hébergement — Dar Khayam", page_icon="🛏️", layout="wide")
 
NAVBAR_CSS = """
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
section[data-testid="stSidebarNav"] {
    display: none !important;
}
.main .block-container {
    padding-top: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}
.dk-navbar {
    background: #0f2744;
    border-bottom: 3px solid #e67e22;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px; height: 60px;
    margin-left: -1.5rem; margin-right: -1.5rem; margin-top: -1rem;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
    position: sticky; top: 0; z-index: 9999;
}
.dk-brand {
    display: flex; align-items: center; gap: 12px;
    text-decoration: none !important;
}
.dk-logo-box {
    width: 38px; height: 38px; background: #e67e22;
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-size: 20px; flex-shrink: 0;
}
.dk-brand-name { color: #fff; font-size: 16px; font-weight: 700; display: block; }
.dk-brand-sub  { color: rgba(255,255,255,0.55); font-size: 11px; display: block; }
.dk-nav { display: flex; align-items: center; height: 100%; gap: 2px; }
.nav-item {
    display: flex; align-items: center; gap: 7px;
    padding: 0 16px; height: 60px;
    color: rgba(255,255,255,0.72); font-size: 13.5px; font-weight: 500;
    text-decoration: none !important;
    border-bottom: 3px solid transparent; margin-bottom: -3px;
    transition: all 0.15s; white-space: nowrap;
}
.nav-item:hover { color:#fff; background:rgba(255,255,255,0.07); border-color:rgba(255,255,255,0.3); }
.nav-item.active { color:#fff; border-color:#e67e22; background:rgba(255,255,255,0.07); }
.dk-user { display:flex; align-items:center; gap:10px; color:rgba(255,255,255,0.7); font-size:13px; font-family:'Segoe UI',sans-serif; }
.dk-avatar { width:34px; height:34px; background:#e67e22; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:white; }
[data-testid="metric-container"] { background:#f8fafd; border:1px solid #e2eaf4; border-radius:10px; padding:16px !important; }
.dept-header { background:linear-gradient(135deg,#0f2744 0%,#1a4a8a 100%); padding:1.2rem 2rem; border-radius:12px; margin-bottom:1.5rem; margin-top:1.2rem; }
.dept-header h2 { color:white !important; margin:0; font-size:1.5rem; }
.dept-header p  { color:#93b4d8; margin:0.3rem 0 0; font-size:0.88rem; }
</style>
"""
 
NAVBAR_HTML = """
<div class="dk-navbar">
    <a href="/" class="dk-brand" target="_self">
        <div class="dk-logo-box">🏨</div>
        <div>
            <span class="dk-brand-name">Dar Khayam</span>
            <span class="dk-brand-sub">Tableau de bord KPI</span>
        </div>
    </a>
    <nav class="dk-nav">
        <a href="/" class="nav-item" target="_self">🏠 Accueil</a>
        <a href="/1_Hebergement" class="nav-item active" target="_self">🛏️ Hébergement</a>
        <a href="/2_Restauration" class="nav-item" target="_self">🍽️ Restauration</a>
        <a href="/3_Ressources_Humaines" class="nav-item" target="_self">👥 Ressources humaines</a>
        <a href="/4_Energie" class="nav-item" target="_self">⚡ Énergie</a>
    </nav>
    <div class="dk-user">
        <span>📅 2024-2025</span>
        <div class="dk-avatar">DK</div>
    </div>
</div>
"""
 
st.markdown(NAVBAR_CSS + NAVBAR_HTML, unsafe_allow_html=True)
 
st.markdown("""
<div class="dept-header">
    <h2>🛏️ Hébergement</h2>
    <p>Taux d'occupation · ADR · RevPAR · Nuitées · Durée moyenne de séjour</p>
</div>
""", unsafe_allow_html=True)
 
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM performance_hotel", conn)
    conn.close()
    return df
 
df = load_data()
 
for col in ["nuitees", "capacite_mensuelle", "nombre_sejours", "chiffre_affaires"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
 
df["taux_occupation"]       = (df["nuitees"] / df["capacite_mensuelle"]) * 100
df["ADR"]                   = df["chiffre_affaires"].div(df["nuitees"].replace(0, pd.NA))
df["RevPAR"]                = df["chiffre_affaires"].div(df["capacite_mensuelle"].replace(0, pd.NA))
df["duree_moyenne_sejour"]  = df["nuitees"].div(df["nombre_sejours"].replace(0, pd.NA))
 
# ── Filtre dans la page (remplace sidebar) ──
with st.expander("🔍 Filtres", expanded=True):
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())
 
df_f = df[df["mois"].isin(mois)]
 
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Chiffre d'affaires", f"{df_f['chiffre_affaires'].sum():,.0f} DT")
c2.metric("🛏️ Nuitées",            f"{df_f['nuitees'].sum():,.0f}")
c3.metric("💵 ADR moyen",          f"{df_f['ADR'].mean():,.2f} DT")
c4.metric("📊 Taux d'occupation",  f"{df_f['taux_occupation'].mean():,.2f} %")
 
st.markdown("---")
 
col_a, col_b = st.columns(2)
 
with col_a:
    st.subheader("📈 Évolution du chiffre d'affaires")
    fig1 = px.line(df_f, x="mois", y="chiffre_affaires", markers=True,
                   color_discrete_sequence=["#1a4a8a"])
    fig1.update_layout(height=320)
    st.plotly_chart(fig1, use_container_width=True)
 
with col_b:
    st.subheader("📊 Taux d'occupation mensuel")
    fig2 = px.bar(df_f, x="mois", y="taux_occupation",
                  color="taux_occupation", color_continuous_scale="Blues")
    fig2.update_layout(height=320)
    st.plotly_chart(fig2, use_container_width=True)
 
st.subheader("💹 ADR et RevPAR")
fig3 = px.line(df_f, x="mois", y=["ADR", "RevPAR"], markers=True,
               color_discrete_sequence=["#1a4a8a", "#e67e22"])
fig3.update_layout(height=320)
st.plotly_chart(fig3, use_container_width=True)
 
st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True)
 
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "hebergement.csv", "text/csv")
