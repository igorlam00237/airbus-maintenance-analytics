"""Classification des lignes Airbus par famille d'appareil, à partir du code modèle.

Les codes modèles FAA (colonne AircraftModel) suivent le format "A3xxYYY..." :
les 4 premiers caractères identifient la famille (A320, A330, A340, A350,
A300, A310, A380). L'A220 (ex-Bombardier CSeries) suit un format différent
("BD5001A10" / "BD5001A11"). Les hélicoptères Airbus Helicopters (EC135,
H160, AS332...) et tout code non reconnu (y compris un éventuel modèle
absent de cette liste) tombent dans un groupe résiduel explicite, à
vérifier au cas par cas plutôt qu'à exclure par hypothèse.
"""

import pandas as pd

# Préfixe (4 premiers caractères du code modèle) -> famille d'appareil.
PREFIXE_VERS_FAMILLE = {
    "A318": "A320",
    "A319": "A320",
    "A320": "A320",
    "A321": "A320",
    "A330": "A330",
    "A340": "A340",
    "A350": "A350",
    "A300": "A300",
    "A310": "A310",
    "A380": "A380",
}


def classify_family(model) -> str:
    """Retourne la famille d'appareil Airbus pour un code modèle donné.

    Valeurs possibles : "A320", "A330", "A340", "A350", "A300", "A310",
    "A380", "A220", "Non_reconnu" (code inattendu, ex: hélicoptère),
    "Non_classe" (modèle manquant dans les données).
    """
    if pd.isna(model):
        return "Non_classe"

    modele = str(model).strip().upper()

    prefixe = modele[:4]
    if prefixe in PREFIXE_VERS_FAMILLE:
        return PREFIXE_VERS_FAMILLE[prefixe]

    if modele.startswith("BD5001A1"):
        return "A220"

    return "Non_reconnu"
