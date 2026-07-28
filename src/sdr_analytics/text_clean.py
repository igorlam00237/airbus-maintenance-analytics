"""Nettoyage du texte libre (`Discrepancy`) avant l'analyse par mots-clés.

Attention : ce texte est en **anglais**, contrairement au reste du projet
(notebooks, commentaires) qui est en français — utiliser une liste de mots
vides anglaise, pas française.
"""

import re

MOTS_VIDES_ANGLAIS = frozenset(
    """
    a about above after again against all am an and any are aren as at be
    because been before being below between both but by can did do does
    doing down during each few for from further had has have having he her
    here hers herself him himself his how i if in into is it its itself
    just me more most my myself no nor not now of off on once only or other
    our ours ourselves out over own re s same she should so some such t
    than that the their theirs them themselves then there these they this
    those through to too under until up very was we were what when where
    which while who whom why will with you your yours yourself yourselves
    """.split()
)
# Remarque : "aren't" est écrit sans apostrophe ("aren") car le tokeniseur
# TF-IDF (comme la plupart) découpe sur la ponctuation avant de comparer
# aux mots vides — une entrée avec apostrophe ne correspondrait jamais.

# Un token qui contient un chiffre est presque toujours une référence de
# pièce, un numéro de série ou un numéro de log — pas du texte narratif.
MOTIF_AVEC_CHIFFRE = re.compile(r"\b\w*\d\w*\b")


def nettoyer_texte(texte) -> str:
    """Met en minuscules et retire les références/numéros avant la
    tokenisation par le vectoriseur TF-IDF."""
    texte = str(texte).lower()
    texte = MOTIF_AVEC_CHIFFRE.sub(" ", texte)
    return texte
