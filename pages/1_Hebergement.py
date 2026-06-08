import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="Hébergement — Dar Khayam", page_icon="🛏️", layout="wide")

# ── Style ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f2744; }
    [data-testid="stSidebar"] * { color: #e8f0fe !important; }
    [data-testid="metric-container"] {
        background: #f8fafd; border: 1px solid #e2eaf4;
        border-radius: 10px; padding: 16px !important;
    }
    .dept-header {
        background: linear-gradient(135deg, #0f2744 0%, #1a4a8a 100%);
        padding: 1.2rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem; color: white;
    }
    .dept-header h2 { color: white !important; margin: 0; font-size: 1.5rem; }
    .dept-header p  { color: #93b4d8; margin: 0.2rem 0 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dept-header">
    <h2>🛏️ Hébergement</h2>
    <p>Taux d'occupation · ADR · RevPAR · Nuitées · Durée moyenne de séjour</p>
</div>
""", unsafe_allow_html=True)

# ── Connexion & données ──────────────────────────────────────────────
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

    df = pd.read_sql("SELECT * FROM performance_hotel", conn)
    conn.close()
    return df

df = load_data()
# ── KPI calculs ──────────────────────────────────────────────────────
df["taux_occupation"]      = (df["nuitees"] / df["capacite_mensuelle"]) * 100
df["ADR"]                  = df["chiffre_affaires"].div(df["nuitees"].replace(0, pd.NA))
df["RevPAR"]               = df["chiffre_affaires"].div(df["capacite_mensuelle"].replace(0, pd.NA))
df["duree_moyenne_sejour"] = df["nuitees"].div(df["nombre_sejours"].replace(0, pd.NA))

# ── Sidebar filtres ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛏️ Hébergement")
    st.markdown("---")
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())

df_f = df[df["mois"].isin(mois)]

# ── KPI cards ────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Chiffre d'affaires",  f"{df_f['chiffre_affaires'].sum():,.0f} DT")
c2.metric("🛏️ Nuitées",             f"{df_f['nuitees'].sum():,.0f}")
c3.metric("💵 ADR moyen",           f"{df_f['ADR'].mean():,.2f} DT")
c4.metric("📊 Taux d'occupation",   f"{df_f['taux_occupation'].mean():,.2f} %")

st.markdown("---")

# ── Graphiques ───────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📈 Évolution du chiffre d'affaires")
    fig1 = px.line(df_f, x="mois", y="chiffre_affaires", markers=True,
                   color_discrete_sequence=["#1a4a8a"])
    fig1.update_layout(xaxis_title="Mois", yaxis_title="CA (DT)", height=320)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("📊 Taux d'occupation mensuel")
    fig2 = px.bar(df_f, x="mois", y="taux_occupation",
                  color="taux_occupation", color_continuous_scale="Blues")
    fig2.update_layout(xaxis_title="Mois", yaxis_title="Taux (%)", height=320)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("💹 ADR et RevPAR")
fig3 = px.line(df_f, x="mois", y=["ADR", "RevPAR"], markers=True,
               color_discrete_sequence=["#1a4a8a", "#e67e22"])
fig3.update_layout(xaxis_title="Mois", yaxis_title="Valeur (DT)", height=320)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True)

csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "hebergement.csv", "text/csv")
