"""Page d'accueil du dashboard Airbus Maintenance Analytics."""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from data_loader import charger_donnees_completes
from sdr_analytics.theme import COULEUR_ACCENT_PRINCIPAL, ENCRE_ATTENUEE, gabarit_plotly

st.set_page_config(
    page_title="Airbus Maintenance Analytics",
    page_icon="✈️",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* Réduire l'espace mort en haut de page */
    .block-container { padding-top: 2.5rem; }

    /* Cartes KPI */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e1e0d9;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }
    div[data-testid="stMetricLabel"] { color: #52514e; }

    /* Bannière d'accueil */
    .hero {
        background: linear-gradient(135deg, #0d366b 0%, #2a78d6 100%);
        border-radius: 14px;
        padding: 2.2rem 2.5rem;
        color: white;
        margin-bottom: 1.8rem;
    }
    .hero h1 { color: white; margin-bottom: 0.4rem; font-size: 2rem; }
    .hero p { color: #e8f1fc; font-size: 1.05rem; margin-bottom: 0; max-width: 800px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>✈️ Airbus Maintenance Analytics</h1>
        <p>
            Cartographie des défaillances de maintenance non programmée sur la flotte Airbus
            actuelle (A320 / A330 / A350), à partir des rapports publics de la FAA — par système
            d'appareil, par âge de flotte, et par motifs récurrents dans les narratifs techniques.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

df = charger_donnees_completes()
df_perimetre = df[df["dans_perimetre"] & df["annee_complete"]]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Signalements analysés", f"{len(df_perimetre):,}".replace(",", " "))
col2.metric("Période couverte", "2015 – 2025")
col3.metric("Familles", "A320 · A330 · A350")
col4.metric("Avions distincts observés", f"{df_perimetre['AircraftSerialNumber'].nunique():,}".replace(",", " "))

st.markdown("")

col_gauche, col_droite = st.columns([3, 2])

with col_gauche:
    st.subheader("Où se concentre le volume de signalements ?")
    comptage = df_perimetre.groupby("libelle_ata").size().sort_values(ascending=False).head(8)
    fig = go.Figure(
        go.Bar(
            x=comptage.values,
            y=comptage.index,
            orientation="h",
            marker_color=COULEUR_ACCENT_PRINCIPAL,
            hovertemplate="%{y} : %{x:,} signalements<extra></extra>",
        )
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Signalements")
    gabarit_plotly(fig, hauteur=320)
    st.plotly_chart(fig, config={"displayModeBar": False})
    st.caption("Le détail complet est dans la page **Cartographie ATA** (menu à gauche).")

with col_droite:
    st.subheader("Comment naviguer")
    st.markdown(
        """
        **📍 Cartographie ATA** — quels systèmes de l'avion sont le plus souvent signalés,
        en comptage brut et en taux normalisé par famille.

        **📈 Âge / Usure** — les pannes changent-elles de nature selon l'âge de l'appareil ?

        **📝 Text Mining** — les mots-clés qui reviennent dans les rapports techniques,
        avec accès aux narratifs bruts.

        **📅 Tendance Temporelle** — évolution 2015-2025, brute et normalisée par taille de flotte.
        """
    )

with st.expander("Source et limites des données"):
    st.markdown(
        """
**Source** : [FAA Service Difficulty Reports (SDR)](https://www.faa.gov/av-info/download_SDR) —
rapports de dysfonctionnements, pannes ou défauts constatés sur des aéronefs, transmis à la FAA
par les compagnies aériennes et ateliers de maintenance.

**Biais géographique assumé** : ces données couvrent uniquement les appareils exploités par des
opérateurs basés aux États-Unis. Les résultats sont un proxy sur la flotte Airbus opérée aux
États-Unis, pas une vision de la flotte Airbus mondiale.

**Périmètre retenu** : familles A320 (incluant A318/A319/A320/A321), A330 et A350 — la flotte
Airbus actuellement produite et commercialisée. A300, A310, A340, A380, A220 et les hélicoptères
Airbus Helicopters sont explicitement exclus.

**Biais de signalement** : le nombre de signalements par avion (utilisé pour normaliser les
comparaisons) sous-estime la vraie taille de flotte — un avion sans aucun problème signalé
n'apparaît jamais dans ces données.

Détail complet des choix méthodologiques : [`docs/methodologie_limites.md`](https://github.com/igorlam00237/airbus-maintenance-analytics/blob/main/docs/methodologie_limites.md).
"""
    )

st.markdown(
    f"<p style='color:{ENCRE_ATTENUEE}; margin-top:1rem;'>"
    "Projet construit avec Python (pandas, scikit-learn), Plotly et Streamlit. "
    "<a href='https://github.com/igorlam00237/airbus-maintenance-analytics'>Code source sur GitHub</a>"
    "</p>",
    unsafe_allow_html=True,
)
