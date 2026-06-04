import streamlit as st

st.set_page_config(
    page_title="Dar Khayam — Dashboard",
    page_icon="🏨",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f2744; }
    [data-testid="stSidebar"] * { color: #e8f0fe !important; }
    [data-testid="metric-container"] {
        background: #f8fafd; border: 1px solid #e2eaf4;
        border-radius: 10px; padding: 16px !important;
    }
    .main-header {
        background: linear-gradient(135deg, #0f2744 0%, #1a4a8a 100%);
        padding: 1.5rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white !important; margin: 0; font-size: 1.8rem; }
    .main-header p  { color: #93b4d8; margin: 0.3rem 0 0; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🏨 Hôtel Dar Khayam</h1>
    <p>Tableau de bord KPI — Sélectionnez un département dans la barre de navigation à gauche</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("🛏️ **Hébergement**\n\nTaux d'occupation, ADR, RevPAR, nuitées")
with col2:
    st.info("🍽️ **Restauration**\n\nFood cost, marge brute, CA F&B")
with col3:
    st.info("👥 **Ressources Humaines**\n\nMasse salariale, productivité, saisonnalité")
with col4:
    st.info("⚡ **Énergie**\n\nÉlectricité, eau, gaz, coûts STEG/SONEDE")

st.markdown("---")
st.caption("Projet de Fin d'Études — Dashboard KPI Informatisé | Hôtel Dar Khayam | 2024-2025")
