"""Vérifie que classify_family() range chaque code modèle dans la bonne famille.

Ce test protège contre une régression du type de celle trouvée dans
l'exploration initiale : une regex mal écrite avait ignoré 47% des lignes
Airbus (tous les A321/A319/A318) sans lever d'erreur.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from sdr_analytics.classify import classify_family


def test_famille_a320_toutes_variantes():
    # A320 est le format sur 4 caractères, pas juste "commence par A32"
    assert classify_family("A320211") == "A320"
    assert classify_family("A321231") == "A320"
    assert classify_family("A319112") == "A320"
    assert classify_family("A318111") == "A320"
    assert classify_family("A321271N") == "A320"  # variante neo


def test_a310_pas_confondu_avec_a320():
    # Piège : "A310" partage le préfixe "A31" avec A318/A319, mais ce n'est
    # pas la même famille (4e caractère différent).
    assert classify_family("A310304") == "A310"


def test_familles_widebody():
    assert classify_family("A330243") == "A330"
    assert classify_family("A330941") == "A330"  # neo
    assert classify_family("A350941") == "A350"


def test_familles_hors_perimetre():
    assert classify_family("A300B4") == "A300"
    assert classify_family("A340*") == "A340"
    assert classify_family("A380841") == "A380"


def test_a220_format_different():
    assert classify_family("BD5001A10") == "A220"
    assert classify_family("BD5001A11") == "A220"


def test_helicoptere_non_confondu_avec_avion():
    assert classify_family("EC135P3") == "Non_reconnu"
    assert classify_family("H160B") == "Non_reconnu"
    assert classify_family("AS332L1") == "Non_reconnu"


def test_valeur_manquante():
    assert classify_family(None) == "Non_classe"
    assert classify_family(pd.NA) == "Non_classe"
    assert classify_family(float("nan")) == "Non_classe"


def test_variante_generique_avec_etoile():
    # Modèle générique/non précisé dans les données brutes (ex: "A320*")
    assert classify_family("A320*") == "A320"
    assert classify_family("A300*") == "A300"
