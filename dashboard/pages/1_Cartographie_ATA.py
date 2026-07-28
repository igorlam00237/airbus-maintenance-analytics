"""Page 1 — Cartographie des défaillances par chapitre ATA."""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_donnees_completes
from sdr_analytics.metrics import pareto_table, taux_pour_1000_avions
from sdr_analytics.theme import (
    COULEUR_ACCENT_PRINCIPAL,
    COULEUR_ACCENT_SECONDAIRE,
    ECHELLE_SEQUENTIELLE,
    gabarit_plotly,
)

st.set_page_config(page_title="Cartographie ATA", page_icon="✈️", layout="wide")
st.title("📍 Cartographie des défaillances par chapitre ATA")
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

# --- Pareto (comptage brut) — un seul axe : tout est en % du total ---
st.subheader("Où se concentre le volume ? (règle des 80/20)")

comptage_brut = df_filtre.groupby("chapitre_ata").size()
pareto = pareto_table(comptage_brut)
libelles = df_filtre[["chapitre_ata", "libelle_ata"]].drop_duplicates().set_index("chapitre_ata")
pareto = pareto.join(libelles).sort_values("nb_signalements", ascending=False)

nb_chapitres_affiches = st.slider("Nombre de chapitres à afficher", 5, 25, 15)
top_n = pareto.head(nb_chapitres_affiches)

fig1 = go.Figure()
fig1.add_bar(
    x=top_n["libelle_ata"],
    y=top_n["part_pct"],
    name="Part du chapitre",
    marker_color=COULEUR_ACCENT_PRINCIPAL,
    customdata=top_n["nb_signalements"],
    hovertemplate="<b>%{x}</b><br>%{customdata:,} signalements (%{y:.1f}% du total)<extra></extra>",
)
fig1.add_scatter(
    x=top_n["libelle_ata"],
    y=top_n["part_cumulee_pct"],
    name="Part cumulée",
    mode="lines+markers",
    line=dict(color=COULEUR_ACCENT_SECONDAIRE, width=2),
    marker=dict(size=8),
    hovertemplate="Cumulé à %{x} : %{y:.1f}%<extra></extra>",
)
fig1.add_hline(y=80, line_dash="dot", line_color="#898781", annotation_text="80%", annotation_position="right")
fig1.update_layout(yaxis_title="% du total des signalements", xaxis_tickangle=-40)
gabarit_plotly(fig1, hauteur=460)
st.plotly_chart(fig1, config={"displayModeBar": False})
st.caption(
    "Les barres et la ligne cumulée sont sur la **même échelle (% du total)** — pas d'axes "
    "doubles, pour ne jamais suggérer une corrélation artificielle entre deux échelles différentes."
)

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
        hide_index=True,
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

    fig2 = go.Figure(
        go.Heatmap(
            z=tableau_taux.values,
            x=tableau_taux.columns,
            y=tableau_taux.index,
            colorscale=ECHELLE_SEQUENTIELLE,
            text=[[f"{v:.0f}" if v == v else "" for v in row] for row in tableau_taux.values],
            texttemplate="%{text}",
            textfont=dict(size=12),
            hovertemplate="%{y} · %{x}<br>%{z:.0f} signalements / 1000 avions<extra></extra>",
            colorbar=dict(title="pour 1000<br>avions"),
        )
    )
    fig2.update_layout(yaxis=dict(autorange="reversed"))
    gabarit_plotly(fig2, hauteur=max(320, len(tableau_taux) * 38))
    st.plotly_chart(fig2, config={"displayModeBar": False})
