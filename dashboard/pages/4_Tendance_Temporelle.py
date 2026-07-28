"""Page 4 — Tendance temporelle des signalements."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_agg_ata, charger_taille_flotte
from sdr_analytics.metrics import pareto_table

st.set_page_config(page_title="Tendance Temporelle", page_icon="✈️", layout="wide")
st.title("Tendance temporelle des signalements")
st.caption(
    "La hausse du nombre de signalements est-elle un vrai signal, ou juste le reflet d'une "
    "flotte qui grandit d'année en année ? On regarde le brut et le normalisé côte à côte."
)

agg_ata = charger_agg_ata()
taille_flotte = charger_taille_flotte()

st.sidebar.header("Filtres")
familles_disponibles = sorted(agg_ata["famille_appareil"].unique())
familles_choisies = st.sidebar.multiselect(
    "Famille d'appareil", familles_disponibles, default=familles_disponibles
)

chapitres_disponibles = agg_ata[["chapitre_ata", "libelle_ata"]].drop_duplicates().sort_values("libelle_ata")
chapitres_choisis_libelles = st.sidebar.multiselect(
    "Chapitres ATA (pour le graphique détaillé ci-dessous — laisser vide = top 6 par défaut)",
    chapitres_disponibles["libelle_ata"].tolist(),
    default=[],
)

if not familles_choisies:
    st.warning("Sélectionnez au moins une famille.")
    st.stop()

agg_filtre = agg_ata[agg_ata["famille_appareil"].isin(familles_choisies)]
flotte_filtree = taille_flotte[taille_flotte["famille_appareil"].isin(familles_choisies)]

# --- Tendance globale : brute vs normalisée ---
st.subheader("Tendance globale : brute vs normalisée")

signalements_par_annee = agg_filtre.groupby("AnneeFichier")["nb_signalements"].sum()
flotte_par_annee = flotte_filtree.groupby("AnneeFichier")["nb_avions_distincts"].sum()

tendance = pd.DataFrame(
    {"nb_signalements": signalements_par_annee, "nb_avions_distincts": flotte_par_annee}
).dropna()
tendance["taux_pour_1000_avions"] = tendance["nb_signalements"] / tendance["nb_avions_distincts"] * 1000

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
ax1.plot(tendance.index, tendance["nb_signalements"], marker="o", color="#4C72B0")
ax1.set_title("Nombre brut de signalements")
ax1.tick_params(axis="x", rotation=45)

ax2.plot(tendance.index, tendance["taux_pour_1000_avions"], marker="o", color="#C44E52")
ax2.set_title("Taux normalisé (pour 1000 avions)")
ax2.tick_params(axis="x", rotation=45)

fig1.tight_layout()
st.pyplot(fig1)

# --- Évolution par chapitre ---
st.subheader("Évolution des chapitres ATA sélectionnés")

if chapitres_choisis_libelles:
    chapitres_a_tracer = chapitres_disponibles.set_index("libelle_ata").loc[
        chapitres_choisis_libelles, "chapitre_ata"
    ].tolist()
else:
    comptage_total = agg_filtre.groupby("chapitre_ata")["nb_signalements"].sum()
    chapitres_a_tracer = pareto_table(comptage_total).head(6).index.tolist()

libelles = agg_filtre[["chapitre_ata", "libelle_ata"]].drop_duplicates().set_index("chapitre_ata")["libelle_ata"]

evolution = (
    agg_filtre[agg_filtre["chapitre_ata"].isin(chapitres_a_tracer)]
    .groupby(["AnneeFichier", "chapitre_ata"])["nb_signalements"]
    .sum()
    .reset_index()
)

fig2, ax = plt.subplots(figsize=(10, 5))
for chapitre in chapitres_a_tracer:
    sous_ensemble = evolution[evolution["chapitre_ata"] == chapitre]
    ax.plot(sous_ensemble["AnneeFichier"], sous_ensemble["nb_signalements"], marker="o", label=libelles[chapitre])
ax.set_ylabel("Nombre de signalements")
plt.xticks(rotation=45)
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
fig2.tight_layout()
st.pyplot(fig2)

# --- Variation YoY ---
with st.expander("Variation d'une année sur l'autre (2 dernières années disponibles)"):
    annees_disponibles = sorted(evolution["AnneeFichier"].unique())
    if len(annees_disponibles) >= 2:
        annee_recente, annee_precedente = annees_disponibles[-1], annees_disponibles[-2]
        pivot = evolution.pivot(index="chapitre_ata", columns="AnneeFichier", values="nb_signalements")
        variation = pd.DataFrame(
            {
                "Chapitre": [libelles[c] for c in pivot.index],
                annee_precedente: pivot[annee_precedente],
                annee_recente: pivot[annee_recente],
            }
        )
        variation["Variation (%)"] = (
            (variation[annee_recente] - variation[annee_precedente]) / variation[annee_precedente] * 100
        )
        st.dataframe(
            variation.sort_values("Variation (%)", ascending=False).round(1),
            width="stretch",
            hide_index=True,
        )
