import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
 
st.set_page_config(page_title="Énergie — Dar Khayam", page_icon="⚡", layout="wide")
 
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
.dk-brand { display:flex; align-items:center; gap:12px; text-decoration:none !important; }
.dk-logo-box { width:38px; height:38px; background:#e67e22; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0; }
.dk-brand-name { color:#fff; font-size:16px; font-weight:700; display:block; }
.dk-brand-sub  { color:rgba(255,255,255,0.55); font-size:11px; display:block; }
.dk-nav { display:flex; align-items:center; height:100%; gap:2px; }
.nav-item {
    display:flex; align-items:center; gap:7px;
    padding:0 16px; height:60px;
    color:rgba(255,255,255,0.72); font-size:13.5px; font-weight:500;
    text-decoration:none !important;
    border-bottom:3px solid transparent; margin-bottom:-3px;
    transition:all 0.15s; white-space:nowrap;
}
.nav-item:hover { color:#fff; background:rgba(255,255,255,0.07); border-color:rgba(255,255,255,0.3); }
.nav-item.active { color:#fff; border-color:#e67e22; background:rgba(255,255,255,0.07); }
.dk-user { display:flex; align-items:center; gap:10px; color:rgba(255,255,255,0.7); font-size:13px; font-family:'Segoe UI',sans-serif; }
.dk-avatar { width:34px; height:34px; background:#e67e22; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:white; }
[data-testid="metric-container"] { background:#f8fafd; border:1px solid #e2eaf4; border-radius:10px; padding:16px !important; }
.dept-header { background:linear-gradient(135deg,#7d6608 0%,#d4ac0d 100%); padding:1.2rem 2rem; border-radius:12px; margin-bottom:1.5rem; margin-top:1.2rem; }
.dept-header h2 { color:white !important; margin:0; font-size:1.5rem; }
.dept-header p  { color:#fef9e7; margin:0.3rem 0 0; font-size:0.88rem; }
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
        <a href="/1_Hebergement" class="nav-item" target="_self">🛏️ Hébergement</a>
        <a href="/2_Restauration" class="nav-item" target="_self">🍽️ Restauration</a>
        <a href="/3_Ressources_Humaines" class="nav-item" target="_self">👥 Ressources humaines</a>
        <a href="/4_Energie" class="nav-item active" target="_self">⚡ Énergie</a>
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
    <h2>⚡ Consommation Énergétique</h2>
    <p>Électricité · Eau · Gaz · Coûts STEG / SONEDE · Analyse saisonnière</p>
</div>
""", unsafe_allow_html=True)
 
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM performance_energetique_hotel", conn)
    conn.close()
    return df
 
df = load_data()
 
nuitees_safe = df["nuitees"].replace(0, pd.NA)
df["elec_par_nuitee"]       = df["electricite_kwh"] / nuitees_safe
df["gaz_par_nuitee"]        = df["gaz_kwh"]         / nuitees_safe
df["eau_par_nuitee"]        = df["eau_m3"]           / nuitees_safe
df["cout_energie_total"]    = df["facture_steg"] + df["facture_sonede"]
df["steg_part_ca_pct"]      = (df["facture_steg"]          / df["chiffre_affaires"]) * 100
df["sonede_part_ca_pct"]    = (df["facture_sonede"]         / df["chiffre_affaires"]) * 100
df["charges_fluides_ca_pct"]= (df["cout_energie_total"]     / df["chiffre_affaires"]) * 100
df["saison"]                = df["mois"].apply(
    lambda x: "Haute saison" if x in ["Juillet", "Août", "Septembre"] else "Basse saison"
)
 
# ── Filtre dans la page ──
with st.expander("🔍 Filtres", expanded=True):
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())
 
df_f = df[df["mois"].isin(mois)]
 
if not df_f.empty:
    mois_max = df_f.loc[df_f["cout_energie_total"].idxmax(), "mois"]
    mois_min = df_f.loc[df_f["cout_energie_total"].idxmin(), "mois"]
    col_i1, col_i2 = st.columns(2)
    col_i1.error(f"📊 Mois le plus coûteux : **{mois_max}**")
    col_i2.success(f"💡 Mois le moins coûteux : **{mois_min}**")
 
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚡ Électricité", f"{df_f['electricite_kwh'].sum():,.0f} kWh")
c2.metric("💧 Eau",         f"{df_f['eau_m3'].sum():,.0f} m³")
c3.metric("🔥 Gaz",         f"{df_f['gaz_kwh'].sum():,.0f} kWh")
c4.metric("💰 Coût total",  f"{df_f['cout_energie_total'].sum():,.0f} TND")
 
st.markdown("---")
 
col_a, col_b = st.columns(2)
 
with col_a:
    st.subheader("⚡ Consommation mensuelle")
    fig1 = px.line(df_f, x="mois", y=["electricite_kwh", "gaz_kwh", "eau_m3"],
                   markers=True, color_discrete_sequence=["#d4ac0d", "#e74c3c", "#2980b9"])
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width=True)
 
with col_b:
    st.subheader("💰 Coûts énergétiques")
    fig2 = px.bar(df_f, x="mois", y="cout_energie_total",
                  color="cout_energie_total", color_continuous_scale="Oranges")
    fig2.update_layout(height=300)
    st.plotly_chart(fig2, use_container_width=True)
 
col_c, col_d = st.columns(2)
 
with col_c:
    st.subheader("📊 CA vs Énergie")
    fig3 = px.line(df_f, x="mois", y=["chiffre_affaires", "cout_energie_total"],
                   markers=True, color_discrete_sequence=["#7d3c98", "#d4ac0d"])
    fig3.update_layout(height=300)
    st.plotly_chart(fig3, use_container_width=True)
 
with col_d:
    st.subheader("🏖️ Haute vs Basse saison")
    seasonal = df_f.groupby("saison")[["cout_energie_total", "chiffre_affaires"]].sum().reset_index()
    fig4 = px.bar(seasonal, x="saison", y=["cout_energie_total", "chiffre_affaires"],
                  barmode="group", color_discrete_sequence=["#d4ac0d", "#7d3c98"])
    fig4.update_layout(height=300)
    st.plotly_chart(fig4, use_container_width=True)
 
st.subheader("📋 Données complètes")
st.dataframe(df_f.round(2), use_container_width=True)
 
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "energie.csv", "text/csv")
