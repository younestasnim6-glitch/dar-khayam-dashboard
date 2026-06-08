import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="Énergie — Dar Khayam", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f2744; }
    [data-testid="stSidebar"] * { color: #e8f0fe !important; }
    [data-testid="metric-container"] {
        background: #f8fafd; border: 1px solid #e2eaf4;
        border-radius: 10px; padding: 16px !important;
    }
    .dept-header {
        background: linear-gradient(135deg, #7d6608 0%, #d4ac0d 100%);
        padding: 1.2rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .dept-header h2 { color: white !important; margin: 0; font-size: 1.5rem; }
    .dept-header p  { color: #fef9e7; margin: 0.2rem 0 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dept-header">
    <h2>⚡ Consommation Énergétique</h2>
    <p>Électricité · Eau · Gaz · Coûts STEG / SONEDE · Analyse saisonnière</p>
</div>
""", unsafe_allow_html=True)

# ── Données ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost", user="root",
        password="Tasnimyns3*", database="hotel_dashboard"
    )
    df = pd.read_sql("SELECT * FROM performance_energetique_hotel", conn)
    conn.close()
    return df

df = load_data()

# ── KPI calculs ──────────────────────────────────────────────────────
nuitees_safe = df["nuitees"].replace(0, pd.NA)
df["elec_par_nuitee"]       = df["electricite_kwh"] / nuitees_safe
df["gaz_par_nuitee"]        = df["gaz_kwh"]         / nuitees_safe
df["eau_par_nuitee"]        = df["eau_m3"]           / nuitees_safe
df["steg_par_nuitee"]       = df["facture_steg"]     / nuitees_safe
df["sonede_par_nuitee"]     = df["facture_sonede"]   / nuitees_safe
df["cout_energie_total"]    = df["facture_steg"] + df["facture_sonede"]
df["steg_part_ca_pct"]      = (df["facture_steg"]          / df["chiffre_affaires"]) * 100
df["sonede_part_ca_pct"]    = (df["facture_sonede"]         / df["chiffre_affaires"]) * 100
df["charges_fluides_ca_pct"]= (df["cout_energie_total"]     / df["chiffre_affaires"]) * 100
df["saison"] = df["mois"].apply(
    lambda x: "Haute saison" if x in ["Juillet", "Août", "Septembre"] else "Basse saison"
)

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ Énergie")
    st.markdown("---")
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())

df_f = df[df["mois"].isin(mois)]

# ── Insights automatiques ─────────────────────────────────────────────
if not df_f.empty:
    mois_max = df_f.loc[df_f["cout_energie_total"].idxmax(), "mois"]
    mois_min = df_f.loc[df_f["cout_energie_total"].idxmin(), "mois"]
    col_i1, col_i2 = st.columns(2)
    col_i1.error(f"📊 Mois le plus coûteux : **{mois_max}**")
    col_i2.success(f"💡 Mois le moins coûteux : **{mois_min}**")

# ── KPI cards ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("⚡ Électricité",   f"{df_f['electricite_kwh'].sum():,.0f} kWh")
c2.metric("💧 Eau",           f"{df_f['eau_m3'].sum():,.0f} m³")
c3.metric("🔥 Gaz",           f"{df_f['gaz_kwh'].sum():,.0f} kWh")
c4.metric("💰 Coût total",    f"{df_f['cout_energie_total'].sum():,.0f} TND")

st.markdown("---")

# ── Graphiques ───────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("⚡ Consommation mensuelle")
    fig1 = px.line(df_f, x="mois", y=["electricite_kwh", "gaz_kwh", "eau_m3"],
                   markers=True,
                   color_discrete_sequence=["#d4ac0d", "#e74c3c", "#2980b9"])
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("💰 Coûts énergétiques")
    fig2 = px.bar(df_f, x="mois", y="cout_energie_total",
                  color="cout_energie_total", color_continuous_scale="Oranges",
                  title="Coût total énergie (STEG + SONEDE)")
    fig2.update_layout(height=300)
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("📊 CA vs Énergie")
    fig3 = px.line(df_f, x="mois", y=["chiffre_affaires", "cout_energie_total"],
                   markers=True,
                   color_discrete_sequence=["#7d3c98", "#d4ac0d"])
    fig3.update_layout(height=300)
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("🏖️ Haute vs Basse saison")
    seasonal = df_f.groupby("saison")[["cout_energie_total", "chiffre_affaires"]].sum().reset_index()
    fig4 = px.bar(seasonal, x="saison", y=["cout_energie_total", "chiffre_affaires"],
                  barmode="group",
                  color_discrete_sequence=["#d4ac0d", "#7d3c98"])
    fig4.update_layout(height=300)
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("📊 KPI détaillés")
st.dataframe(
    df_f[["mois","elec_par_nuitee","gaz_par_nuitee","eau_par_nuitee",
          "steg_par_nuitee","sonede_par_nuitee","steg_part_ca_pct",
          "sonede_part_ca_pct","cout_energie_total","charges_fluides_ca_pct"]].round(2),
    use_container_width=True
)

st.subheader("📋 Données complètes")
st.dataframe(df_f.round(2), use_container_width=True)

csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "energie.csv", "text/csv")

