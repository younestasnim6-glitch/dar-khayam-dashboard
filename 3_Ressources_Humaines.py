import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
 
st.set_page_config(page_title="Ressources Humaines — Dar Khayam", page_icon="👥", layout="wide")
 
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
.dept-header { background:linear-gradient(135deg,#145a32 0%,#1e8449 100%); padding:1.2rem 2rem; border-radius:12px; margin-bottom:1.5rem; margin-top:1.2rem; }
.dept-header h2 { color:white !important; margin:0; font-size:1.5rem; }
.dept-header p  { color:#a9dfbf; margin:0.3rem 0 0; font-size:0.88rem; }
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
        <a href="/3_Ressources_Humaines" class="nav-item active" target="_self">👥 Ressources humaines</a>
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
    <h2>👥 Ressources Humaines</h2>
    <p>Masse salariale · Productivité · Coût salarial · Analyse saisonnière</p>
</div>
""", unsafe_allow_html=True)
 
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM rh_hotel_clean", conn)
    conn.close()
    return df
 
df = load_data()
 
df["chiffre_affaires"]          = pd.to_numeric(df["chiffre_affaires"])
df["masse_salariale"]           = pd.to_numeric(df["masse_salariale"])
df["nombre_effectifs"]          = pd.to_numeric(df["nombre_effectifs"])
df["productivite_par_employe"]  = df["chiffre_affaires"] / df["nombre_effectifs"]
df["cout_salarial_pct"]         = (df["masse_salariale"] / df["chiffre_affaires"]) * 100
 
def saison(mois):
    if mois in ["Juillet", "Août"]:      return "Haute saison"
    elif mois in ["Juin", "Septembre"]:  return "Moyenne saison"
    else:                                return "Basse saison"
 
df["saison"] = df["mois"].apply(saison)
 
# ── Filtres dans la page ──
with st.expander("🔍 Filtres", expanded=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())
    with col_f2:
        saisons = st.multiselect("Saison", df["saison"].unique(), default=df["saison"].unique())
 
df_f = df[df["mois"].isin(mois) & df["saison"].isin(saisons)]
 
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 CA Total",          f"{df_f['chiffre_affaires'].sum():,.0f} DT")
c2.metric("💼 Masse salariale",   f"{df_f['masse_salariale'].sum():,.0f} DT")
c3.metric("👤 Productivité moy.", f"{df_f['productivite_par_employe'].mean():,.2f} DT")
c4.metric("📊 Coût salarial %",  f"{df_f['cout_salarial_pct'].mean():.2f} %")
 
st.markdown("---")
 
col_a, col_b = st.columns(2)
 
with col_a:
    st.subheader("📈 CA mensuel")
    fig1 = px.line(df_f, x="mois", y="chiffre_affaires", markers=True,
                   color_discrete_sequence=["#1e8449"])
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width=True)
 
with col_b:
    st.subheader("📊 CA vs Masse salariale")
    fig2 = px.bar(df_f, x="mois", y=["chiffre_affaires", "masse_salariale"],
                  barmode="group", color_discrete_sequence=["#1e8449", "#e67e22"])
    fig2.update_layout(height=300)
    st.plotly_chart(fig2, use_container_width=True)
 
col_c, col_d = st.columns(2)
 
with col_c:
    st.subheader("👨‍💼 Productivité par employé")
    fig3 = px.bar(df_f, x="mois", y="productivite_par_employe",
                  color="productivite_par_employe", color_continuous_scale="Greens")
    fig3.update_layout(height=300)
    st.plotly_chart(fig3, use_container_width=True)
 
with col_d:
    st.subheader("🌞 Répartition par saison")
    season_kpi = df_f.groupby("saison")["chiffre_affaires"].mean().reset_index()
    fig4 = px.pie(season_kpi, names="saison", values="chiffre_affaires",
                  color_discrete_sequence=["#1e8449", "#f39c12", "#2980b9"])
    fig4.update_layout(height=300)
    st.plotly_chart(fig4, use_container_width=True)
 
st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True)
 
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "rh.csv", "text/csv")
