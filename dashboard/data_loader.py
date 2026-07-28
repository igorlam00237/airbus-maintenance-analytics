"""Chargement des données pour le dashboard.

Le dashboard ne recalcule rien : il lit les fichiers déjà préparés par les
notebooks (dossier data/processed). Les fonctions sont mises en cache par
Streamlit pour ne charger chaque fichier qu'une seule fois.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# Racine du projet = dossier parent de dashboard/. On résout les chemins par
# rapport à ce fichier pour que ça marche quel que soit le dossier de lancement
# (en local comme sur Streamlit Community Cloud).
RACINE_PROJET = Path(__file__).resolve().parents[1]
CHEMIN_TRAITEES = RACINE_PROJET / "data" / "processed"
CHEMIN_REFERENCE = RACINE_PROJET / "data" / "reference"


@st.cache_data
def charger_donnees_completes() -> pd.DataFrame:
    """Le jeu de données ligne par ligne (pour les KPI et le drill-down texte)."""
    return pd.read_parquet(CHEMIN_TRAITEES / "sdr_airbus_clean.parquet")


@st.cache_data
def charger_agg_ata() -> pd.DataFrame:
    """Comptage des signalements par chapitre ATA x famille x année."""
    return pd.read_parquet(CHEMIN_TRAITEES / "agg_ata_famille_annee.parquet")


@st.cache_data
def charger_taille_flotte() -> pd.DataFrame:
    """Nombre d'avions distincts observés par famille x année."""
    return pd.read_parquet(CHEMIN_TRAITEES / "agg_taille_flotte.parquet")


@st.cache_data
def charger_top_termes() -> pd.DataFrame:
    """Termes les plus caractéristiques par chapitre (text mining)."""
    return pd.read_parquet(CHEMIN_TRAITEES / "agg_top_termes_chapitre.parquet")


@st.cache_data
def charger_glossaire() -> pd.DataFrame:
    """Glossaire des abréviations de maintenance."""
    return pd.read_csv(CHEMIN_REFERENCE / "glossaire_abreviations.csv")
