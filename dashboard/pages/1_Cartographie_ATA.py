"""Page 1 — Cartographie des défaillances par chapitre ATA."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_donnees_completes
from sdr_analytics.metrics import pareto_table, taux_pour_1000_avions

st.set_page_config(page_title="Cartographie ATA", page_icon="✈️", layout="wide")
st.title("Cartographie des défaillances par chapitre ATA")
st.caption(
    "Où se concentre le volume de signalements (comptage brut), et quels chapitres sont "
    "sur-représentés une fois ramené à la taille de chaque flotte (taux normalisé) ?"
)

df = charger_donnees_completes()
df_perimetre = df[df["dans_perimetre"] & df["annee_complete"]]

# --- Filtres ---
familles_disponibles = sorted(df_perimetre["famille_appareil"].unique())
annees_disponibles = sorted(df_perimetre["AnneeFichier"].unique())

st.sidebar.header("Filtres")
familles_choisies = st.sidebar.multiselect(
    "Famille d'appareil", familles_disponibles, default=familles_disponibles
)
periode = st.sidebar.select_slider(
    "Période",
    options=annees_disponibles,
    value=(annees_disponibles[0], annees_disponibles[-1]),
)

df_filtre = df_perimetre[
    df_perimetre["famille_appareil"].isin(familles_choisies)
    & df_perimetre["AnneeFichier"].between(periode[0], periode[1])
]

if df_filtre.empty:
    st.warning("Aucune donnée pour cette combinaison de filtres.")
    st.stop()

st.caption(f"{len(df_filtre):,} signalements dans la sélection actuelle".replace(",", " "))

# --- Pareto (comptage brut) ---
st.subheader("Où se concentre le volume ? (comptage brut)")

comptage_brut = df_filtre.groupby("chapitre_ata").size()
pareto = pareto_table(comptage_brut)
libelles = df_filtre[["chapitre_ata", "libelle_ata"]].drop_duplicates().set_index("chapitre_ata")
pareto = pareto.join(libelles)

nb_chapitres_affiches = st.slider("Nombre de chapitres à afficher", 5, 25, 15)
top_n = pareto.head(nb_chapitres_affiches)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(top_n["libelle_ata"], top_n["nb_signalements"], color="#4C72B0")
ax1.set_ylabel("Nombre de signalements")
ax1.set_xticks(range(len(top_n)))
ax1.set_xticklabels(top_n["libelle_ata"], rotation=45, ha="right")

ax2 = ax1.twinx()
ax2.plot(top_n["libelle_ata"], top_n["part_cumulee_pct"], color="#C44E52", marker="o")
ax2.axhline(80, color="gray", linestyle="--", linewidth=1)
ax2.set_ylabel("Part cumulée (%)")
ax2.set_ylim(0, 105)
fig1.tight_layout()
st.pyplot(fig1)

with st.expander("Table détaillée"):
    st.dataframe(
        top_n[["libelle_ata", "nb_signalements", "part_pct", "part_cumulee_pct"]].rename(
            columns={
                "libelle_ata": "Chapitre",
                "nb_signalements": "Signalements",
                "part_pct": "Part (%)",
                "part_cumulee_pct": "Part cumulée (%)",
            }
        ).round(1),
        width="stretch",
    )

# --- Taux normalisé ---
st.subheader("Comparer les familles entre elles (taux normalisé)")
st.caption(
    "Nombre de signalements pour 1000 avions distincts observés — pas un vrai taux de panne "
    "(un avion sans aucun signalement n'apparaît jamais dans ces données), mais un indicateur "
    "de comparaison relative entre familles."
)

if len(familles_choisies) < 2:
    st.info("Sélectionnez au moins 2 familles pour comparer les taux normalisés.")
else:
    avions_distincts = df_filtre.groupby("famille_appareil")["AircraftSerialNumber"].nunique()

    chapitres_top = top_n.index.tolist()
    comptage_croise = (
        df_filtre[df_filtre["chapitre_ata"].isin(chapitres_top)]
        .groupby(["chapitre_ata", "famille_appareil"])
        .size()
        .rename("nb_signalements")
        .reset_index()
    )
    comptage_croise["nb_avions_distincts"] = comptage_croise["famille_appareil"].map(avions_distincts)
    comptage_croise["taux"] = taux_pour_1000_avions(
        comptage_croise["nb_signalements"], comptage_croise["nb_avions_distincts"]
    )

    tableau_taux = comptage_croise.pivot(index="chapitre_ata", columns="famille_appareil", values="taux")
    tableau_taux = tableau_taux.reindex(chapitres_top)
    tableau_taux.index = tableau_taux.index.map(libelles["libelle_ata"])

    fig2, ax = plt.subplots(figsize=(6, max(4, len(tableau_taux) * 0.4)))
    im = ax.imshow(tableau_taux.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(tableau_taux.columns)))
    ax.set_xticklabels(tableau_taux.columns)
    ax.set_yticks(range(len(tableau_taux.index)))
    ax.set_yticklabels(tableau_taux.index)
    for i in range(tableau_taux.shape[0]):
        for j in range(tableau_taux.shape[1]):
            valeur = tableau_taux.values[i, j]
            if not np.isnan(valeur):
                ax.text(j, i, f"{valeur:.0f}", ha="center", va="center", fontsize=8)
    plt.colorbar(im, ax=ax, label="Signalements pour 1000 avions")
    fig2.tight_layout()
    st.pyplot(fig2)
