import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

st.set_page_config(page_title="Restauration — Dar Khayam", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f2744; }
    [data-testid="stSidebar"] * { color: #e8f0fe !important; }
    [data-testid="metric-container"] {
        background: #f8fafd; border: 1px solid #e2eaf4;
        border-radius: 10px; padding: 16px !important;
    }
    .dept-header {
        background: linear-gradient(135deg, #7b2d00 0%, #c0392b 100%);
        padding: 1.2rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
    }
    .dept-header h2 { color: white !important; margin: 0; font-size: 1.5rem; }
    .dept-header p  { color: #f5b7b1; margin: 0.2rem 0 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dept-header">
    <h2>🍽️ Restauration — F&B</h2>
    <p>Food cost · Beverage cost · Marge brute · Chiffre d'affaires</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM couts_fb", conn)
    conn.close()
    return df

df = load_data()

df["total_achats"]    = df["achats_nourriture"] + df["achats_boissons"]
df["food_cost_%"]     = (df["achats_nourriture"] / df["chiffre_affaires"]) * 100
df["beverage_cost_%"] = (df["achats_boissons"]   / df["chiffre_affaires"]) * 100
df["marge_brute"]     = df["chiffre_affaires"] - df["total_achats"]
df["profit_%"]        = (df["marge_brute"]        / df["chiffre_affaires"]) * 100

with st.sidebar:
    st.markdown("### 🍽️ Restauration")
    st.markdown("---")
    mois = st.multiselect("Mois", df["mois"].unique(), default=df["mois"].unique())

df_f = df[df["mois"].isin(mois)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 CA Total",            f"{df_f['chiffre_affaires'].sum():,.0f} TND")
c2.metric("🍽️ Food Cost moyen",     f"{df_f['food_cost_%'].mean():.2f} %")
c3.metric("🍹 Beverage Cost moyen", f"{df_f['beverage_cost_%'].mean():.2f} %")
c4.metric("📊 Profit moyen",        f"{df_f['profit_%'].mean():.2f} %")

st.markdown("---")
if df_f["food_cost_%"].mean() > 35:
    st.error("⚠️ Food Cost trop élevé (> 35%)")
else:
    st.success("✅ Food Cost sous contrôle (< 35%)")

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📈 Chiffre d'affaires mensuel")
    fig1 = px.line(df_f, x="mois", y="chiffre_affaires", markers=True,
                   color_discrete_sequence=["#c0392b"])
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("🍽️ Food Cost %")
    fig2 = px.bar(df_f, x="mois", y="food_cost_%",
                  color="food_cost_%", color_continuous_scale="Reds")
    fig2.update_layout(height=300)
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)
with col_c:
    st.subheader("💰 Marge brute mensuelle")
    fig3 = px.bar(df_f, x="mois", y="marge_brute",
                  color="marge_brute", color_continuous_scale="Greens")
    fig3.update_layout(height=300)
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("🥘 Répartition des achats")
    fig4 = px.pie(
        values=[df_f["achats_nourriture"].sum(), df_f["achats_boissons"].sum()],
        names=["Nourriture", "Boissons"],
        color_discrete_sequence=["#c0392b", "#e67e22"]
    )
    fig4.update_layout(height=300)
    st.plotly_chart(fig4, use_container_width=True)

best = df_f.loc[df_f["chiffre_affaires"].idxmax(), "mois"] if not df_f.empty else "—"
st.info(f"🏆 Meilleur mois : **{best}**")

st.subheader("📋 Données détaillées")
st.dataframe(df_f.round(2), use_container_width=True)

csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "restauration.csv", "text/csv")
