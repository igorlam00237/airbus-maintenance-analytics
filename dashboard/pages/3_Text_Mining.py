"""Page 3 — Text mining sur les narratifs techniques."""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from data_loader import charger_donnees_completes, charger_glossaire, charger_top_termes
from sdr_analytics.theme import COULEUR_ACCENT_PRINCIPAL, gabarit_plotly

st.set_page_config(page_title="Text Mining", page_icon="✈️", layout="wide")
st.title("📝 Text mining sur les narratifs techniques")
st.caption(
    "Mots et expressions les plus caractéristiques de chaque chapitre ATA, extraits du texte "
    "libre écrit par les techniciens (TF-IDF, calculé à l'avance — pas recalculé ici pour "
    "rester réactif)."
)

top_termes = charger_top_termes()
df = charger_donnees_completes()
df_perimetre = df[df["dans_perimetre"] & df["annee_complete"]]

chapitres_disponibles = (
    top_termes[["chapitre_ata", "libelle_ata"]]
    .drop_duplicates()
    .sort_values("libelle_ata")
)

st.sidebar.header("Filtres")
chapitre_choisi_libelle = st.sidebar.selectbox(
    "Chapitre ATA", chapitres_disponibles["libelle_ata"].tolist()
)
chapitre_choisi = chapitres_disponibles.set_index("libelle_ata").loc[chapitre_choisi_libelle, "chapitre_ata"]

# --- Termes caractéristiques ---
st.subheader(f"Termes caractéristiques — {chapitre_choisi_libelle}")

termes_chapitre = top_termes[top_termes["chapitre_ata"] == chapitre_choisi].sort_values(
    "score", ascending=True
)

fig = go.Figure(
    go.Bar(
        x=termes_chapitre["score"],
        y=termes_chapitre["terme"],
        orientation="h",
        marker_color=COULEUR_ACCENT_PRINCIPAL,
        hovertemplate="\"%{y}\" — score TF-IDF %{x:.3f}<extra></extra>",
    )
)
fig.update_layout(xaxis_title="Score TF-IDF moyen")
gabarit_plotly(fig, hauteur=340)
st.plotly_chart(fig, config={"displayModeBar": False})

# --- Drill-down : vrais narratifs ---
st.subheader("Voir des signalements réels")

terme_recherche = st.text_input(
    "Rechercher un terme dans les narratifs de ce chapitre",
    value=termes_chapitre["terme"].iloc[-1] if not termes_chapitre.empty else "",
)

if terme_recherche:
    correspondances = df_perimetre[
        (df_perimetre["chapitre_ata"] == chapitre_choisi)
        & df_perimetre["Discrepancy"].str.contains(terme_recherche, case=False, na=False)
    ]
    st.caption(f"{len(correspondances)} signalement(s) trouvé(s) contenant \"{terme_recherche}\"")
    for texte in correspondances["Discrepancy"].head(10):
        st.markdown(f"> {texte}")
        st.markdown("---")

# --- Glossaire ---
with st.expander("📖 Glossaire des abréviations de maintenance"):
    st.dataframe(charger_glossaire(), width="stretch", hide_index=True)
