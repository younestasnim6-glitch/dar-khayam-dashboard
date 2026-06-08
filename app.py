import streamlit as st

st.set_page_config(
    page_title="Dar Khayam — Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ─────────────────────────────
# CSS
# ─────────────────────────────
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

/* Header */
.dept-header {
    background: linear-gradient(135deg, #0f2744 0%, #1a4a8a 100%);
    padding: 1.2rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    margin-top: 1.2rem;
}

.dept-header h2 {
    color: white !important;
    margin: 0;
    font-size: 1.5rem;
}

.dept-header p {
    color: #93b4d8;
    margin: 0.3rem 0 0;
    font-size: 0.88rem;
}

/* Metrics */
[data-testid="metric-container"] {
    background: #f8fafd;
    border: 1px solid #e2eaf4;
    border-radius: 10px;
    padding: 16px !important;
}
</style>
"""

st.markdown(NAVBAR_CSS, unsafe_allow_html=True)

# ─────────────────────────────
# NAVIGATION
# ─────────────────────────────
page = st.selectbox("Navigation", [
    "Accueil",
    "Hébergement",
    "Restauration",
    "Ressources humaines",
    "Énergie"
])

if page == "Accueil":

    st.markdown("""
    <div class="dept-header">
        <h2>🏨 Hôtel Dar Khayam</h2>
        <p>Tableau de bord KPI global — Sélectionnez un département</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("🛏️ Hébergement")

    with col2:
        st.info("🍽️ Restauration")

    with col3:
        st.info("👥 Ressources humaines")

    with col4:
        st.info("⚡ Énergie")

elif page == "Hébergement":
    st.warning("➡ Accédez au dashboard Hébergement (page séparée ou à intégrer ici)")

elif page == "Restauration":
    st.warning("➡ Accédez au dashboard Restauration")

elif page == "Ressources humaines":
    st.warning("➡ Accédez au dashboard RH")

elif page == "Énergie":
    st.warning("➡ Accédez au dashboard Énergie")
    

# ─────────────────────────────
# FOOTER
# ─────────────────────────────
st.markdown("---")
st.caption("Projet de Fin d'Études — Dashboard KPI Hôtel Dar Khayam | 2024-2025")
