"""Constantes partagées par les notebooks et le dashboard."""

from pathlib import Path

# Racine du projet (deux niveaux au-dessus de ce fichier : src/sdr_analytics/config.py -> racine)
RACINE_PROJET = Path(__file__).resolve().parents[2]

CHEMIN_DONNEES_BRUTES = RACINE_PROJET / "data" / "raw"
CHEMIN_DONNEES_REFERENCE = RACINE_PROJET / "data" / "reference"
CHEMIN_DONNEES_TRAITEES = RACINE_PROJET / "data" / "processed"

# Familles d'appareils Airbus retenues dans le périmètre de l'analyse.
# Décision actée avec Igor le 28/07/2026 : on se limite à la flotte Airbus
# actuellement produite (A320/A330/A350). L'A300/A310/A380 sont des
# générations antérieures ou en fin de vie ; l'A220 est une conception
# d'origine Bombardier, pas une ingénierie Airbus native.
FAMILLES_DANS_PERIMETRE = {"A320", "A330", "A350"}

# Seuils de plausibilité pour AircraftTotalCycles / AircraftTotalTime.
# Au-delà, la valeur est considérée comme une erreur de saisie (voir
# investigation initiale : max observé de 5,68M cycles / 9,25M heures,
# alors que ~99% des valeurs se situent sous 40 000 cycles / 90 000 heures).
SEUIL_MAX_CYCLES_PLAUSIBLE = 150_000
SEUIL_MAX_HEURES_PLAUSIBLE = 150_000

# Année en cours au moment de l'analyse (2026) : données partielles
# (janvier-juillet uniquement), à exclure des comparaisons année sur année.
ANNEE_PARTIELLE = "2026"
