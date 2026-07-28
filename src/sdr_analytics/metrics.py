"""Calculs réutilisés dans les notebooks d'analyse et le dashboard.

Ces fonctions ne font rien de statistiquement compliqué exprès : l'objectif
du projet est que chaque calcul reste explicable simplement, pas d'utiliser
la méthode la plus sophistiquée possible.
"""

import pandas as pd


def pareto_table(comptages: pd.Series) -> pd.DataFrame:
    """À partir d'une série de comptages (index = catégorie, ex: chapitre ATA),
    retourne un tableau trié du plus fréquent au moins fréquent, avec la part
    en % et la part cumulée en % — la base d'un diagramme de Pareto (règle
    des 80/20)."""
    table = comptages.sort_values(ascending=False).rename("nb_signalements").to_frame()
    table["part_pct"] = table["nb_signalements"] / table["nb_signalements"].sum() * 100
    table["part_cumulee_pct"] = table["part_pct"].cumsum()
    return table


def taux_pour_1000_avions(nb_signalements: pd.Series, nb_avions_distincts: pd.Series) -> pd.Series:
    """Calcule un taux de signalements pour 1000 avions distincts observés.

    Attention, ce n'est PAS un vrai taux de panne : le dénominateur (nombre
    d'avions distincts qui apparaissent dans les données SDR) sous-estime la
    vraie taille de flotte, puisqu'un avion sans aucun signalement n'apparaît
    jamais dans ces données. C'est un indicateur de comparaison relative
    entre familles/années, pas une mesure de fiabilité absolue.
    """
    return nb_signalements / nb_avions_distincts * 1000
