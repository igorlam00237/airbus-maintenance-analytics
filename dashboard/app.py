"""Page d'accueil du dashboard Airbus Maintenance Analytics."""

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
from data_loader import charger_donnees_completes

st.set_page_config(
    page_title="Airbus Maintenance Analytics",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Airbus Maintenance Analytics")

st.markdown(
    """
Cartographie des défaillances de maintenance non programmée sur la flotte Airbus actuelle
(A320 / A330 / A350), à partir des rapports publics de la FAA (Federal Aviation Administration) :
par système d'appareil (chapitre ATA), par âge de flotte, et par motifs récurrents dans les
narratifs techniques.

Utilisez le menu à gauche pour naviguer entre les analyses.
"""
)

with st.expander("Source et limites des données", expanded=False):
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

Détail complet des choix méthodologiques : `docs/methodologie_limites.md` dans le dépôt du projet.
"""
    )

df = charger_donnees_completes()
df_perimetre = df[df["dans_perimetre"] & df["annee_complete"]]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Signalements analysés", f"{len(df_perimetre):,}".replace(",", " "))
col2.metric("Période couverte", "2015 - 2025")
col3.metric("Familles", "A320 / A330 / A350")
col4.metric("Avions distincts observés", f"{df_perimetre['AircraftSerialNumber'].nunique():,}".replace(",", " "))

st.markdown("---")
st.markdown(
    "Projet construit avec Python (pandas, scikit-learn) et Streamlit. "
    "[Code source sur GitHub](https://github.com/igorlam00237/airbus-maintenance-analytics)"
)
