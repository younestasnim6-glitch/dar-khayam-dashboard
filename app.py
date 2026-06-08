import streamlit as st
 
st.set_page_config(
    page_title="Dar Khayam — Dashboard",
    page_icon="🏨",
    layout="wide"
)
 
NAVBAR_CSS = """
<style>
/* Masquer la sidebar et le bouton collapse */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
section[data-testid="stSidebarNav"] {
    display: none !important;
}
 
/* Réduire le padding top */
.main .block-container {
    padding-top: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}
 
/* ── Navbar ── */
.dk-navbar {
    background: #0f2744;
    border-bottom: 3px solid #e67e22;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px;
    height: 60px;
    margin-left: -1.5rem;
    margin-right: -1.5rem;
    margin-top: -1rem;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
    position: sticky;
    top: 0;
    z-index: 9999;
}
 
.dk-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none !important;
}
.dk-logo-box {
    width: 38px; height: 38px;
    background: #e67e22;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.dk-brand-name {
    color: #ffffff;
    font-size: 16px; font-weight: 700;
    letter-spacing: 0.3px; display: block;
}
.dk-brand-sub {
    color: rgba(255,255,255,0.55);
    font-size: 11px; display: block;
}
 
.dk-nav {
    display: flex;
    align-items: center;
    height: 100%;
    gap: 2px;
}
.nav-item {
    display: flex; align-items: center; gap: 7px;
    padding: 0 16px;
    height: 60px;
    color: rgba(255,255,255,0.72);
    font-size: 13.5px; font-weight: 500;
    text-decoration: none !important;
    border-bottom: 3px solid transparent;
    margin-bottom: -3px;
    transition: all 0.15s;
    white-space: nowrap;
}
.nav-item:hover {
    color: #fff;
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.3);
}
.nav-item.active {
    color: #ffffff;
    border-color: #e67e22;
    background: rgba(255,255,255,0.07);
}
 
.dk-user {
    display: flex; align-items: center; gap: 10px;
    color: rgba(255,255,255,0.7);
    font-size: 13px; font-family: 'Segoe UI', sans-serif;
}
.dk-avatar {
    width: 34px; height: 34px;
    background: #e67e22; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: white;
}
 
/* ── Métriques ── */
[data-testid="metric-container"] {
    background: #f8fafd;
    border: 1px solid #e2eaf4;
    border-radius: 10px;
    padding: 16px !important;
}
 
/* ── En-tête département ── */
.dept-header {
    background: linear-gradient(135deg, #0f2744 0%, #1a4a8a 100%);
    padding: 1.2rem 2rem; border-radius: 12px;
    margin-bottom: 1.5rem; margin-top: 1.2rem;
}
.dept-header h2 { color: white !important; margin: 0; font-size: 1.5rem; }
.dept-header p { color: #93b4d8; margin: 0.3rem 0 0; font-size: 0.88rem; }
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
        <a href="/" class="nav-item active" target="_self">🏠 Accueil</a>
        <a href="/1_Hebergement" class="nav-item" target="_self">🛏️ Hébergement</a>
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
 
# ── Contenu de la page d'accueil ──
st.markdown("""
<div class="dept-header">
    <h2>🏨 Hôtel Dar Khayam</h2>
    <p>Tableau de bord KPI — Sélectionnez un département dans la barre de navigation ci-dessus</p>
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
