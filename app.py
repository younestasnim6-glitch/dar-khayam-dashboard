import streamlit as st

st.set_page_config(
    page_title="Dar Khayam — Dashboard KPI",
    page_icon="🏨",
    layout="wide"
)

st.markdown("""
<style>
    /* Cacher sidebar */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Fond général */
    .stApp { background-color: #f7f9fc; }

    /* ── TOPBAR ── */
    .topbar {
        background: white;
        border-bottom: 2px solid #e8f0fe;
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin-bottom: 0;
        flex-wrap: wrap;
    }
    .topbar-logo {
        font-size: 1.05rem;
        font-weight: 800;
        color: #E65100;
        white-space: nowrap;
        letter-spacing: -0.3px;
    }
    .topbar-sep { color: #dde3f0; font-size: 1.3rem; }
    .nav-link {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 18px; border-radius: 99px;
        background: #fff8f0; border: 1.5px solid #ffcc99;
        color: #E65100 !important; font-size: 0.84rem;
        font-weight: 600; text-decoration: none !important; white-space: nowrap;
        transition: all 0.15s;
    }
    .nav-link:hover {
        background: #E65100; color: white !important; border-color: #E65100;
    }

    /* ── HERO BANNER ── */
    .hero {
        background: linear-gradient(135deg, #1565C0 0%, #1E88E5 50%, #E65100 100%);
        padding: 3rem 3rem 2.5rem;
        border-radius: 0 0 28px 28px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -60px; right: 120px;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        color: white !important;
        padding: 4px 16px; border-radius: 99px;
        font-size: 0.78rem; font-weight: 600;
        margin-bottom: 1rem; letter-spacing: 0.04em;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .hero h1 {
        color: white !important;
        font-size: 2.6rem; font-weight: 800;
        margin: 0 0 0.5rem; line-height: 1.15;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem; margin: 0 0 1.5rem;
    }
    .hero-chips { display: flex; gap: 10px; flex-wrap: wrap; }
    .hero-chip {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        color: white !important; padding: 5px 14px;
        border-radius: 99px; font-size: 0.8rem; font-weight: 500;
    }

    /* ── ALERTE SAISONNALITÉ ── */
    .season-alert {
        background: linear-gradient(90deg, #fff8f0 0%, #fff3e0 100%);
        border: 2px solid #FFB74D;
        border-left: 6px solid #E65100;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.8rem;
        display: flex; align-items: center; gap: 1rem;
        flex-wrap: wrap;
    }
    .season-alert-icon { font-size: 1.8rem; }
    .season-alert-text { flex: 1; }
    .season-alert-text strong { color: #E65100; }
    .season-alert-text span { color: #5a3a00; font-size: 0.9rem; }

    /* ── MÉTRIQUES GLOBALES ── */
    .metrics-title {
        font-size: 0.72rem; font-weight: 700; color: #90A4AE;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 0.8rem;
    }
    [data-testid="metric-container"] {
        background: white !important;
        border: 1.5px solid #e8f0fe !important;
        border-top: 4px solid #1E88E5 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }
    [data-testid="metric-container"]:nth-child(5) {
        border-top-color: #E65100 !important;
    }

    /* ── CARTES DÉPARTEMENT ── */
    .section-label {
        font-size: 0.72rem; font-weight: 700; color: #90A4AE;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin: 2rem 0 1rem;
    }
    .dept-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    .dept-card {
        background: white;
        border-radius: 16px;
        padding: 1.6rem;
        border: 1.5px solid #e8f0fe;
        border-top: 5px solid;
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s;
    }
    .dept-card::after {
        content: attr(data-icon);
        position: absolute;
        right: 16px; bottom: 12px;
        font-size: 3.5rem;
        opacity: 0.07;
        line-height: 1;
    }
    .dept-card.blue   { border-top-color: #1E88E5; }
    .dept-card.red    { border-top-color: #E53935; }
    .dept-card.orange { border-top-color: #E65100; }
    .dept-card.green  { border-top-color: #2E7D32; }
    .dept-card-header {
        display: flex; align-items: center;
        gap: 12px; margin-bottom: 0.8rem;
    }
    .dept-icon-circle {
        width: 44px; height: 44px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; flex-shrink: 0;
    }
    .dept-icon-circle.blue   { background: #e3f2fd; }
    .dept-icon-circle.red    { background: #ffebee; }
    .dept-icon-circle.orange { background: #fff3e0; }
    .dept-icon-circle.green  { background: #e8f5e9; }
    .dept-title {
        font-size: 1.05rem; font-weight: 700; color: #1a2a3a; margin: 0;
    }
    .dept-sub {
        font-size: 0.82rem; color: #78909C;
        line-height: 1.55; margin-bottom: 1rem;
    }
    .dept-kpis { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1rem; }
    .dept-kpi-tag {
        font-size: 0.72rem; padding: 3px 10px;
        border-radius: 99px; font-weight: 600;
        border: 1px solid;
    }
    .dept-kpi-tag.blue   { background:#e3f2fd; color:#1565C0; border-color:#90CAF9; }
    .dept-kpi-tag.red    { background:#ffebee; color:#C62828; border-color:#EF9A9A; }
    .dept-kpi-tag.orange { background:#fff3e0; color:#E65100; border-color:#FFCC80; }
    .dept-kpi-tag.green  { background:#e8f5e9; color:#2E7D32; border-color:#A5D6A7; }
    .dept-stat-row {
        display: flex; gap: 16px;
        padding-top: 0.9rem;
        border-top: 1px solid #f0f4f8;
    }
    .dept-stat { text-align: left; }
    .dept-stat-val { font-size: 1.1rem; font-weight: 700; color: #1a2a3a; }
    .dept-stat-lbl { font-size: 0.72rem; color: #90A4AE; margin-top: 1px; }

    /* ── BANDE PROJET ── */
    .project-band {
        background: linear-gradient(90deg, #1565C0 0%, #E65100 100%);
        border-radius: 14px;
        padding: 1.4rem 2rem;
        margin: 2rem 0 1rem;
        display: flex; align-items: center;
        justify-content: space-between; flex-wrap: wrap; gap: 1rem;
    }
    .project-band-left h3 {
        color: white !important; margin: 0 0 0.2rem;
        font-size: 1rem; font-weight: 700;
    }
    .project-band-left p {
        color: rgba(255,255,255,0.8); margin: 0; font-size: 0.83rem;
    }
    .project-band-right {
        display: flex; gap: 10px; flex-wrap: wrap;
    }
    .project-chip {
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        color: white !important; padding: 5px 14px;
        border-radius: 99px; font-size: 0.78rem; font-weight: 600;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center; color: #B0BEC5;
        font-size: 0.76rem; margin-top: 1.5rem;
        padding-top: 1rem; border-top: 1px solid #e8f0fe;
    }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <span class="topbar-logo">🏨 DAR KHAYAM</span>
    <span class="topbar-sep">|</span>
    <a class="nav-link" href="/1_Hebergement">🛏️ Hébergement</a>
    <a class="nav-link" href="/2_Restauration">🍽️ Restauration</a>
    <a class="nav-link" href="/3_Ressources_Humaines">👥 Ressources Humaines</a>
    <a class="nav-link" href="/4_Energie">⚡ Énergie</a>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">📊 Projet de Fin d'Études — ISET Nabeul 2024–2025</div>
    <h1>Tableau de bord<br>de performance hôtelière</h1>
    <p class="hero-sub">Suivi et analyse des KPI de l'Hôtel Dar Khayam — Hammamet Nord</p>
    <div class="hero-chips">
        <span class="hero-chip">📍 Hammamet Nord</span>
        <span class="hero-chip">⭐⭐⭐ 3 étoiles</span>
        <span class="hero-chip">🍽️ Formule Tout Inclus</span>
        <span class="hero-chip">🛏️ 321 chambres</span>
        <span class="hero-chip">👥 140 employés permanents</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ALERTE SAISONNALITÉ ───────────────────────────────────────────────────
st.markdown("""
<div class="season-alert">
    <span class="season-alert-icon">🌊</span>
    <div class="season-alert-text">
        <strong>Impact saisonnalité :</strong>
        <span> La <strong>haute saison (Juil–Sep)</strong> génère <strong>56.4 %</strong>
        du CA annuel. En janvier, le coût salarial dépasse <strong>265 %</strong> du CA.
        Le Food Cost d'avril atteint <strong>100.22 %</strong> — marge négative de 703 TND.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MÉTRIQUES GLOBALES ────────────────────────────────────────────────────
st.markdown('<p class="metrics-title">📊 Résultats globaux — Exercice 2025</p>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🛏️ Nuitées totales",  "55 933",     "exercice complet")
c2.metric("💰 CA hébergement",   "8.94 M TND", "pic : août")
c3.metric("📈 Taux occupation",  "54.2 %",     "max 93.66 % août")
c4.metric("💹 RevPAR moyen",     "84.67 TND",  "min 4.11 TND jan")
c5.metric("🍽️ Food Cost moy.",   "50.4 %",     "⚠ avr : 100.22 %")

# ── CARTES DÉPARTEMENT ────────────────────────────────────────────────────
st.markdown('<p class="section-label">🏢 Sélectionnez un département à analyser</p>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="dept-card blue" data-icon="🛏️">
        <div class="dept-card-header">
            <div class="dept-icon-circle blue">🛏️</div>
            <div>
                <p class="dept-title">Hébergement</p>
            </div>
        </div>
        <p class="dept-sub">
            Analyse de l'occupation des chambres, des revenus par nuitée
            et de l'impact de la saisonnalité sur les indicateurs clés.
        </p>
        <div class="dept-kpis">
            <span class="dept-kpi-tag blue">Taux d'occupation</span>
            <span class="dept-kpi-tag blue">ADR</span>
            <span class="dept-kpi-tag blue">RevPAR</span>
            <span class="dept-kpi-tag blue">Durée séjour</span>
        </div>
        <div class="dept-stat-row">
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#1E88E5;">93.66 %</div>
                <div class="dept-stat-lbl">Pic occupation (août)</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#1E88E5;">84.67 TND</div>
                <div class="dept-stat-lbl">RevPAR maximum</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#1E88E5;">55 933</div>
                <div class="dept-stat-lbl">Nuitées annuelles</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Hebergement.py", label="📊 Ouvrir le département Hébergement",
                 use_container_width=True)

with col2:
    st.markdown("""
    <div class="dept-card red" data-icon="🍽️">
        <div class="dept-card-header">
            <div class="dept-icon-circle red">🍽️</div>
            <div>
                <p class="dept-title">Restauration F&B</p>
            </div>
        </div>
        <p class="dept-sub">
            Suivi du Food Cost, Beverage Cost et de la marge brute mensuelle.
            Analyse critique du mois d'avril (marge négative).
        </p>
        <div class="dept-kpis">
            <span class="dept-kpi-tag red">Food Cost %</span>
            <span class="dept-kpi-tag red">Beverage Cost %</span>
            <span class="dept-kpi-tag red">Marge brute</span>
            <span class="dept-kpi-tag red">Total Cost %</span>
        </div>
        <div class="dept-stat-row">
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E53935;">50.42 %</div>
                <div class="dept-stat-lbl">Food Cost annuel</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E53935;">1.36 M TND</div>
                <div class="dept-stat-lbl">Marge brute août</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E53935;">-703 TND</div>
                <div class="dept-stat-lbl">Marge brute avril</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Restauration.py", label="📊 Ouvrir le département Restauration",
                 use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="dept-card orange" data-icon="👥">
        <div class="dept-card-header">
            <div class="dept-icon-circle orange">👥</div>
            <div>
                <p class="dept-title">Ressources Humaines</p>
            </div>
        </div>
        <p class="dept-sub">
            Analyse de la productivité par employé, du coût salarial
            et de l'impact de la saisonnalité sur les effectifs (123 à 449 employés).
        </p>
        <div class="dept-kpis">
            <span class="dept-kpi-tag orange">Productivité/emp.</span>
            <span class="dept-kpi-tag orange">Coût salarial %</span>
            <span class="dept-kpi-tag orange">Masse salariale</span>
        </div>
        <div class="dept-stat-row">
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E65100;">5 868 TND</div>
                <div class="dept-stat-lbl">Productivité/emp. août</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E65100;">265 %</div>
                <div class="dept-stat-lbl">Coût salarial janvier</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#E65100;">449</div>
                <div class="dept-stat-lbl">Effectif max (juillet)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Ressources_Humaines.py", label="📊 Ouvrir le département RH",
                 use_container_width=True)

with col4:
    st.markdown("""
    <div class="dept-card green" data-icon="⚡">
        <div class="dept-card-header">
            <div class="dept-icon-circle green">⚡</div>
            <div>
                <p class="dept-title">Énergie</p>
            </div>
        </div>
        <p class="dept-sub">
            Consommation STEG et SONEDE rapportée aux nuitées.
            Analyse de l'effet d'échelle entre haute et basse saison.
        </p>
        <div class="dept-kpis">
            <span class="dept-kpi-tag green">Élec./nuitée</span>
            <span class="dept-kpi-tag green">Eau/nuitée</span>
            <span class="dept-kpi-tag green">Part STEG/CA</span>
            <span class="dept-kpi-tag green">Charges fluides %</span>
        </div>
        <div class="dept-stat-row">
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#2E7D32;">136 TND</div>
                <div class="dept-stat-lbl">Énergie/nuitée janvier</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#2E7D32;">6.85 TND</div>
                <div class="dept-stat-lbl">Énergie/nuitée sept.</div>
            </div>
            <div class="dept-stat">
                <div class="dept-stat-val" style="color:#2E7D32;">103 %</div>
                <div class="dept-stat-lbl">Fluides/CA janvier</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Energie.py", label="📊 Ouvrir le département Énergie",
                 use_container_width=True)

# ── BANDE PROJET ──────────────────────────────────────────────────────────
st.markdown("""
<div class="project-band">
    <div class="project-band-left">
        <h3>🎓 Projet de Fin d'Études — Techniques Comptables & Financières</h3>
        <p>ISET Nabeul · Département Sciences Économiques & Gestion · 2024–2025</p>
    </div>
    <div class="project-band-right">
        <span class="project-chip">🐍 Python / Pandas</span>
        <span class="project-chip">🗄️ MySQL</span>
        <span class="project-chip">📊 Streamlit</span>
        <span class="project-chip">📈 Plotly</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Réalisé par <strong>Tasnim YOUNES & Malek MOHI EDDINE</strong> ·
    Encadrées par <strong>Mme. Saloua BANI</strong> (académique) &
    <strong>Mme. Imen MAJDOUB</strong> (professionnelle)<br>
    Hôtel Dar Khayam · Hammamet Nord · Tunisie
</div>
""", unsafe_allow_html=True)


