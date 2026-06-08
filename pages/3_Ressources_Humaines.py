import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="Ressources Humaines — Dar Khayam", page_icon="👥", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f2744; }
    [data-testid="stSidebar"] * { color: #e8f0fe !important; }
    [data-testid="metric-container"] {
        background: #f8fafd; border: 1px solid #e2eaf4;
        border-radius: 10px; padding: 16px !important;
    }
    .dept-header {
        background: linear-gradient(135deg, #145a32 0%, #1e8449 100%);
        padding: 1.2rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .dept-header h2 { color: white !important; margin: 0; font-size: 1.5rem; }
    .dept-header p  { color: #a9dfbf; margin: 0.2rem 0 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dept-header">
    <h2>👥 Ressources Humaines</h2>
    <p>Masse salariale · Productivité · Coût salarial · Analyse saisonnière</p>
</div>
""", unsafe_allow_html=True)

# ── Données ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"]),
        ssl_disabled=True
    )

    df = pd.read_sql("SELECT * FROM rh_hotel_clean", conn)
    conn.close()
    return df

df = load_data()

df["chiffre_affaires"] = pd.to_numeric(df["chiffre_affaires"], errors="coerce")
df["masse_salariale"] = pd.to_numeric(df["masse_salariale"], errors="coerce")
df["nombre_effectifs"] = pd.to_numeric(df["nombre_effectifs"], errors="coerce")

# ── KPI calculs ──────────────────────────────────────────────────────
df["productivite_par_employe"]    = df["chiffre_affaires"] / df["nombre_effectifs"]
df["cout_salarial_pct"]           = (df["masse_salariale"] / df["chiffre_affaires"]) * 100
df["masse_salariale_par_employe"] = df["masse_salariale"]  / df["nombre_effectifs"]

def saison(mois):
    if mois in ["Juillet", "Août"]:        return "Haute saison"
    elif mois in ["Juin", "Septembre"]:    return "Moyenne saison"
    else:                                  return "Basse saison"

df["saison"] = df["mois"].apply(saison)

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👥 Ressources Humaines")
    st.markdown("---")
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())
    saisons = st.multiselect("Saison", df["saison"].unique(), default=df["saison"].unique())

df_f = df[df["mois"].isin(mois) & df["saison"].isin(saisons)]

# ── KPI cards ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
total_ca = df_f["chiffre_affaires"].sum()

c1.metric(
    "💰 Chiffre d'affaires",
    f"{total_ca:,.0f}".replace(",", " ") + " DT"
)
c2.metric("💼 Masse salariale",    f"{df_f['masse_salariale'].sum():,.0f} DT")
c3.metric("👤 Productivité moy.", f"{df_f['productivite_par_employe'].mean():,.2f} DT")
c4.metric("📊 Coût salarial %",    f"{df_f['cout_salarial_pct'].mean():.2f} %")

st.markdown("---")

# ── Graphiques ───────────────────────────────────────────────────────
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
                  barmode="group",
                  color_discrete_sequence=["#1e8449", "#e67e22"])
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

st.subheader("📊 KPI par saison")
st.dataframe(
    df_f.groupby("saison")[["chiffre_affaires","masse_salariale",
                             "productivite_par_employe","cout_salarial_pct"]].mean().round(2),
    use_container_width=True
)

st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True)

csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "rh.csv", "text/csv")

