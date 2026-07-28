"""Palette de couleurs et style visuel partagés par tout le dashboard.

Palette validée (contraste, daltonisme) — voir le rapport de validation dans
le journal du projet. Les couleurs catégorielles sont assignées dans un ordre
fixe, jamais généré à la volée : chaque famille d'appareil garde toujours la
même couleur, sur toutes les pages du dashboard.
"""

# --- Encre et surfaces ---
ENCRE_PRIMAIRE = "#0b0b0b"
ENCRE_SECONDAIRE = "#52514e"
ENCRE_ATTENUEE = "#898781"
SURFACE = "#fcfcfb"
GRILLE = "#e1e0d9"

# --- Palette catégorielle (ordre fixe, validé) ---
PALETTE_CATEGORIELLE = [
    "#2a78d6",  # 1 bleu
    "#1baf7a",  # 2 aqua
    "#eda100",  # 3 jaune
    "#008300",  # 4 vert
    "#4a3aa7",  # 5 violet
    "#e34948",  # 6 rouge
    "#e87ba4",  # 7 magenta
    "#eb6834",  # 8 orange
]

# Une famille = une couleur, fixe sur tout le dashboard.
COULEUR_FAMILLE = {
    "A320": PALETTE_CATEGORIELLE[0],
    "A330": PALETTE_CATEGORIELLE[1],
    "A350": PALETTE_CATEGORIELLE[2],
}

COULEUR_ACCENT_PRINCIPAL = PALETTE_CATEGORIELLE[0]   # bleu — série unique par défaut
COULEUR_ACCENT_SECONDAIRE = PALETTE_CATEGORIELLE[5]  # rouge — deuxième mesure (ex: cumulé)

# --- Échelle séquentielle (une teinte, clair -> foncé) — pour les comparaisons de magnitude ---
ECHELLE_SEQUENTIELLE = [
    [0.0, "#e8f1fc"],
    [0.25, "#9ec5f4"],
    [0.5, "#5598e7"],
    [0.75, "#2a78d6"],
    [1.0, "#0d366b"],
]

# --- Échelle divergente (bleu <-> rouge, centre neutre gris) — pour les métriques avec un point neutre (ex: lift = 1.0) ---
ECHELLE_DIVERGENTE = [
    [0.0, "#0d366b"],
    [0.25, "#5598e7"],
    [0.5, "#f0efec"],
    [0.75, "#ef9a94"],
    [1.0, "#e34948"],
]

POLICE = "system-ui, -apple-system, 'Segoe UI', sans-serif"


def gabarit_plotly(fig, hauteur=None):
    """Applique le style visuel commun à une figure Plotly : police, fond,
    grille discrète, marges. À appeler juste avant st.plotly_chart()."""
    fig.update_layout(
        font=dict(family=POLICE, color=ENCRE_PRIMAIRE, size=13),
        plot_bgcolor=SURFACE,
        paper_bgcolor=SURFACE,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family=POLICE),
    )
    fig.update_xaxes(gridcolor=GRILLE, zeroline=False, showline=True, linecolor=GRILLE)
    fig.update_yaxes(gridcolor=GRILLE, zeroline=False, showline=False)
    if hauteur:
        fig.update_layout(height=hauteur)
    return fig
