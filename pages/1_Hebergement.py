import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import GLOBAL_CSS, sidebar_logo, dept_header
 
st.set_page_config(page_title="Hébergement — Dar Khayam", page_icon="🛏️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
 
# ── Sidebar ──────────────────────────────────────────────────────────
sidebar_logo("🛏️", "Hébergement")
 
# ── Header ───────────────────────────────────────────────────────────
dept_header(
    icon="🛏️",
    title="Hébergement",
    subtitle="Taux d'occupation · ADR · RevPAR · Nuitées · Durée moyenne de séjour",
    gradient="linear-gradient(135deg, #1565c0 0%, #1976d2 60%, #42a5f5 100%)"
)
 
# ── Données ───────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def load_data():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root",
            password="Tasnimyns3*", database="hotel_dashboard"
        )
        df = pd.read_sql("SELECT * FROM performance_hotel", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erreur de connexion : {e}")
        return pd.DataFrame()
 
df = load_data()
if df.empty:
    st.stop()
 
for col in ["nuitees", "capacite_mensuelle", "nombre_sejours", "chiffre_affaires"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
 
df["taux_occupation"]      = (df["nuitees"] / df["capacite_mensuelle"]) * 100
df["ADR"]                  = df["chiffre_affaires"].div(df["nuitees"].replace(0, pd.NA))
df["RevPAR"]               = df["chiffre_affaires"].div(df["capacite_mensuelle"].replace(0, pd.NA))
df["duree_moyenne_sejour"] = df["nuitees"].div(df["nombre_sejours"].replace(0, pd.NA))
 
# ── Sidebar filtres ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### 🔍 Filtres")
    mois_options = df["mois"].unique().tolist()
    mois = st.multiselect("Mois", mois_options, default=mois_options)
    st.markdown("---")
    st.caption("💡 Sélectionnez un ou plusieurs mois pour filtrer les données.")
 
df_f = df[df["mois"].isin(mois)]
 
# ── Alertes intelligentes ─────────────────────────────────────────────
occ_moy = df_f["taux_occupation"].mean()
if not df_f.empty:
    col_a1, col_a2 = st.columns(2)
    if occ_moy >= 80:
        col_a1.success(f"✅ Taux d'occupation excellent : **{occ_moy:.1f}%**")
    elif occ_moy >= 60:
        col_a1.warning(f"⚠️ Taux d'occupation moyen : **{occ_moy:.1f}%**")
    else:
        col_a1.error(f"🔴 Taux d'occupation faible : **{occ_moy:.1f}%**")
 
    mois_peak = df_f.loc[df_f["chiffre_affaires"].idxmax(), "mois"] if not df_f.empty else "—"
    col_a2.info(f"🏆 Meilleur mois CA : **{mois_peak}**")
 
st.markdown("---")
 
# ── KPI cards ─────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Chiffre d'affaires",  f"{df_f['chiffre_affaires'].sum():,.0f} DT")
c2.metric("🛏️ Nuitées",             f"{df_f['nuitees'].sum():,.0f}")
c3.metric("💵 ADR moyen",           f"{df_f['ADR'].mean():,.2f} DT")
c4.metric("📊 Taux d'occupation",   f"{df_f['taux_occupation'].mean():,.1f} %")
c5.metric("📅 Durée moy. séjour",   f"{df_f['duree_moyenne_sejour'].mean():,.1f} nuits")
 
st.markdown("---")
 
# ── Graphiques ────────────────────────────────────────────────────────
BLUE   = "#1565c0"
ORANGE = "#e67e22"
LBLUE  = "#42a5f5"
 
col_a, col_b = st.columns(2)
 
with col_a:
    st.subheader("📈 Évolution du chiffre d'affaires")
    fig1 = px.area(df_f, x="mois", y="chiffre_affaires", markers=True,
                   color_discrete_sequence=[BLUE])
    fig1.update_traces(fill='tozeroy', fillcolor='rgba(21,101,192,0.10)')
    fig1.update_layout(xaxis_title="Mois", yaxis_title="CA (DT)", height=300,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis=dict(gridcolor="#f0f4ff"), yaxis=dict(gridcolor="#f0f4ff"))
    st.plotly_chart(fig1, use_container_width=True)
 
with col_b:
    st.subheader("📊 Taux d'occupation mensuel")
    fig2 = px.bar(df_f, x="mois", y="taux_occupation",
                  color="taux_occupation",
                  color_continuous_scale=[[0,"#bbdefb"],[0.5,"#1976d2"],[1,"#0d47a1"]])
    fig2.add_hline(y=80, line_dash="dash", line_color=ORANGE,
                   annotation_text="Objectif 80%", annotation_font_color=ORANGE)
    fig2.update_layout(xaxis_title="Mois", yaxis_title="Taux (%)", height=300,
                       plot_bgcolor="white", paper_bgcolor="white",
                       xaxis=dict(gridcolor="#f0f4ff"), yaxis=dict(gridcolor="#f0f4ff"))
    st.plotly_chart(fig2, use_container_width=True)
 
st.subheader("💹 ADR et RevPAR comparatifs")
fig3 = px.line(df_f, x="mois", y=["ADR", "RevPAR"], markers=True,
               color_discrete_sequence=[BLUE, ORANGE])
fig3.update_traces(line_width=2.5)
fig3.update_layout(xaxis_title="Mois", yaxis_title="Valeur (DT)", height=300,
                   plot_bgcolor="white", paper_bgcolor="white",
                   legend_title="Indicateur",
                   xaxis=dict(gridcolor="#f0f4ff"), yaxis=dict(gridcolor="#f0f4ff"))
st.plotly_chart(fig3, use_container_width=True)
 
# ── Données & export ──────────────────────────────────────────────────
st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True, height=280)
 
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "hebergement.csv", "text/csv")
