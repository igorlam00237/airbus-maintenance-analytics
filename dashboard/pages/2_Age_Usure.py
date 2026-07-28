"""Page 2 — Âge de l'appareil vs profil de pannes."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_donnees_completes
from sdr_analytics.metrics import pareto_table

st.set_page_config(page_title="Âge / Usure", page_icon="✈️", layout="wide")
st.title("Âge de l'appareil vs profil de pannes")
st.caption(
    "Certains chapitres ATA sont-ils plutôt des défauts de jeunesse, ou plutôt de l'usure "
    "qui s'accumule avec les cycles de vol ?"
)

df = charger_donnees_completes()
df_perimetre = df[df["dans_perimetre"] & df["annee_complete"]]

st.sidebar.header("Filtres")
familles_disponibles = sorted(df_perimetre["famille_appareil"].unique())
familles_choisies = st.sidebar.multiselect(
    "Famille d'appareil", familles_disponibles, default=familles_disponibles
)

df_age = df_perimetre[
    df_perimetre["famille_appareil"].isin(familles_choisies)
    & df_perimetre["AircraftTotalCycles"].notna()
].copy()

if df_age.empty or len(familles_choisies) == 0:
    st.warning("Aucune donnée pour cette sélection.")
    st.stop()

st.caption(
    f"{len(df_age):,} signalements avec un nombre de cycles connu".replace(",", " ")
)


def tercile_par_groupe(cycles):
    return pd.qcut(cycles, 3, labels=["jeune", "mature", "âgé"], duplicates="drop")


df_age["tranche_age"] = df_age.groupby("famille_appareil")["AircraftTotalCycles"].transform(
    tercile_par_groupe
)

# --- Distribution des cycles par famille ---
st.subheader("Distribution des cycles par famille")
st.caption(
    "Les tranches (jeune/mature/âgé) sont calculées séparément pour chaque famille : un A350 "
    "long-courrier accumule des cycles bien plus lentement qu'un A320 court-courrier, donc un "
    "seuil unique classerait presque tous les A350 comme \"jeunes\" à tort."
)

fig1, axes = plt.subplots(1, len(familles_choisies), figsize=(5 * len(familles_choisies), 4), squeeze=False)
for ax, (famille, groupe) in zip(axes[0], df_age.groupby("famille_appareil")):
    ax.hist(groupe["AircraftTotalCycles"], bins=30, color="#4C72B0")
    ax.set_title(famille)
    ax.set_xlabel("Cycles")
axes[0][0].set_ylabel("Nombre de signalements")
fig1.tight_layout()
st.pyplot(fig1)

# --- Lift par chapitre x tranche ---
st.subheader("Chapitres sur/sous-représentés selon l'âge")
st.caption(
    "Lift = signalements observés ÷ signalements attendus si l'âge n'avait aucun lien avec le "
    "chapitre. Lift > 1 : plus signalé que la moyenne pour cette tranche. Lift < 1 : moins signalé."
)

nb_chapitres = st.slider("Nombre de chapitres à afficher", 5, 20, 10)
top_chapitres = pareto_table(df_age.groupby("chapitre_ata").size()).head(nb_chapitres).index.tolist()
libelles = df_age[["chapitre_ata", "libelle_ata"]].drop_duplicates().set_index("chapitre_ata")["libelle_ata"]

sous_ensemble = df_age[df_age["chapitre_ata"].isin(top_chapitres)]
comptage = sous_ensemble.groupby(["chapitre_ata", "tranche_age"], observed=True).size().rename("observe").reset_index()
total_par_chapitre = sous_ensemble.groupby("chapitre_ata").size().rename("total_chapitre")
total_par_tranche = sous_ensemble.groupby("tranche_age", observed=True).size().rename("total_tranche")
total_general = len(sous_ensemble)

comptage = comptage.merge(total_par_chapitre, on="chapitre_ata").merge(total_par_tranche, on="tranche_age")
comptage["attendu"] = comptage["total_chapitre"] * comptage["total_tranche"] / total_general
comptage["lift"] = comptage["observe"] / comptage["attendu"]

tableau_lift = comptage.pivot(index="chapitre_ata", columns="tranche_age", values="lift")
tableau_lift = tableau_lift.reindex(top_chapitres)
colonnes_ordre = [c for c in ["jeune", "mature", "âgé"] if c in tableau_lift.columns]
tableau_lift = tableau_lift[colonnes_ordre]
tableau_lift.index = tableau_lift.index.map(libelles)

fig2, ax = plt.subplots(figsize=(6, max(4, len(tableau_lift) * 0.4)))
im = ax.imshow(tableau_lift.values, cmap="RdBu_r", vmin=0.5, vmax=1.5, aspect="auto")
ax.set_xticks(range(len(tableau_lift.columns)))
ax.set_xticklabels(tableau_lift.columns)
ax.set_yticks(range(len(tableau_lift.index)))
ax.set_yticklabels(tableau_lift.index)
for i in range(tableau_lift.shape[0]):
    for j in range(tableau_lift.shape[1]):
        valeur = tableau_lift.values[i, j]
        if not np.isnan(valeur):
            ax.text(j, i, f"{valeur:.2f}", ha="center", va="center", fontsize=8)
plt.colorbar(im, ax=ax, label="Lift (observé / attendu)")
fig2.tight_layout()
st.pyplot(fig2)
