"""Page 2 — Âge de l'appareil vs profil de pannes."""

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_donnees_completes
from sdr_analytics.metrics import pareto_table
from sdr_analytics.theme import COULEUR_FAMILLE, ECHELLE_DIVERGENTE, gabarit_plotly

st.set_page_config(page_title="Âge / Usure", page_icon="✈️", layout="wide")
st.title("📈 Âge de l'appareil vs profil de pannes")
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

fig1 = make_subplots(rows=1, cols=len(familles_choisies), subplot_titles=familles_choisies)
for i, famille in enumerate(familles_choisies, start=1):
    valeurs = df_age.loc[df_age["famille_appareil"] == famille, "AircraftTotalCycles"]
    fig1.add_histogram(
        x=valeurs,
        marker_color=COULEUR_FAMILLE.get(famille, "#2a78d6"),
        nbinsx=30,
        row=1,
        col=i,
        showlegend=False,
        hovertemplate="%{x} cycles<br>%{y} signalements<extra></extra>",
    )
    fig1.update_xaxes(title_text="Cycles", row=1, col=i)
fig1.update_yaxes(title_text="Signalements", row=1, col=1)
gabarit_plotly(fig1, hauteur=320)
st.plotly_chart(fig1, config={"displayModeBar": False})

# --- Lift par chapitre x tranche ---
st.subheader("Chapitres sur/sous-représentés selon l'âge")
st.caption(
    "Lift = signalements observés ÷ signalements attendus si l'âge n'avait aucun lien avec le "
    "chapitre. **Bleu = moins signalé que la moyenne, rouge = plus signalé.** Blanc = aucun lien avec l'âge (lift = 1)."
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

fig2 = go.Figure(
    go.Heatmap(
        z=tableau_lift.values,
        x=tableau_lift.columns,
        y=tableau_lift.index,
        colorscale=ECHELLE_DIVERGENTE,
        zmid=1.0,
        zmin=0.5,
        zmax=1.5,
        text=[[f"{v:.2f}" if v == v else "" for v in row] for row in tableau_lift.values],
        texttemplate="%{text}",
        textfont=dict(size=12),
        hovertemplate="%{y} · %{x}<br>lift = %{z:.2f}<extra></extra>",
        colorbar=dict(title="lift"),
    )
)
fig2.update_layout(yaxis=dict(autorange="reversed"))
gabarit_plotly(fig2, hauteur=max(320, len(tableau_lift) * 38))
st.plotly_chart(fig2, config={"displayModeBar": False})
