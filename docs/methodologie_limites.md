# Méthodologie et limites

Ce document explique les choix faits pendant la construction de l'analyse, et leurs limites. Objectif : que chaque chiffre présenté puisse être expliqué et défendu, pas juste montré.

*Document vivant — complété au fur et à mesure de l'avancement du projet.*

## 1. Source et biais géographique

Les données proviennent des [FAA Service Difficulty Reports](https://www.faa.gov/av-info/download_SDR) (SDR), le système de signalement de la FAA (autorité de l'aviation civile américaine). **Ces données ne couvrent que les appareils exploités par des opérateurs basés aux États-Unis.** Les résultats de ce projet sont donc un proxy sur la flotte Airbus opérée aux États-Unis, pas une vision représentative de la flotte Airbus mondiale — ce biais est assumé explicitement plutôt que dissimulé.

## 2. Biais du signalement événementiel

Un signalement SDR n'existe que si un problème a été constaté et déclaré. Cela a deux conséquences directes sur la lecture des résultats :

- Le nombre de signalements par appareil/famille/chapitre ATA reflète ce qui a été **signalé**, pas nécessairement tout ce qui s'est produit.
- L'indicateur de "taille de flotte" utilisé pour normaliser les comparaisons (nombre de numéros de série d'avion distincts observés) **sous-estime la vraie flotte** : un avion sans aucun signalement n'apparaît jamais dans les données, donc n'est jamais compté.

## 3. Périmètre : familles retenues et exclues

Périmètre retenu : **A320** (incluant A318/A319/A320/A321, variantes ceo et neo), **A330**, **A350** — la flotte Airbus actuellement produite et commercialisée.

Comptage exact des familles identifiées dans les données (Airbus, toutes années 2015-2025, avant tout nettoyage) :

| Famille | Lignes | Décision | Raison |
|---|---|---|---|
| A320 | 97 794 | Retenue | — |
| A300 | 16 636 | Exclue | Génération antérieure, production arrêtée en 2007 |
| A330 | 13 742 | Retenue | — |
| A220 | 2 903 | Exclue | Conception d'origine Bombardier (C Series), pas une ingénierie Airbus native |
| A350 | 659 | Retenue (avec réserve, voir §4) | — |
| A310 | 186 | Exclue | Génération antérieure, production arrêtée en 1998 |
| Hélicoptères (Airbus Helicopters) | 20 | Exclue (donnée retirée) | Catégorie d'appareil différente, pas un avion de ligne |
| A380 | 19 | Exclue | Production arrêtée en 2021, échantillon négligeable |
| Modèle manquant | 3 | Exclue (donnée retirée) | Impossible à classer |
| A340 | 1 | Exclue | Génération de l'A330, production arrêtée ~2011 |

Le choix de se limiter à A320/A330/A350 a été acté avant de connaître ces chiffres exacts — notamment le volume de l'A300 (plus gros que A330+A350 réunis), qui aurait pu passer inaperçu si on ne l'avait pas explicitement vérifié.

**Anomalie mineure notée en cours de nettoyage** : 4 lignes isolées portent un code de chapitre ATA normalement réservé aux hélicoptères (rotors/hélices) alors qu'elles ne sont pas classées comme hélicoptères — probablement des erreurs de saisie ponctuelles dans les données source. Elles concernent uniquement des familles déjà hors périmètre (A300, A220), donc sans impact sur l'analyse.

## 4. Échantillon réduit pour l'A350

L'A350 a un historique de service plus court dans ces données : 0 signalement en 2015-2016, seulement 2 avions distincts identifiés en 2017, montant progressivement à 33 avions distincts en 2025. Toute lecture comparative impliquant l'A350 sur les premières années du jeu de données doit être accompagnée de cette réserve — ce n'est pas un problème de qualité de donnée, juste un historique de flotte plus court.

## 5. Codes non vérifiés : `NatureOfConditionA`

Le champ `NatureOfConditionA` (nature de la panne : codes lettre O, J, L, B...) n'a pas de définition publique trouvée. Recherche effectuée : requête web ciblée, récupération et lecture du document officiel FAA "SDRS Field Instructions" (formulaire FAA 8070-1). Ce document confirme la structure du champ mais renvoie systématiquement vers une liste déroulante interne au site de saisie, jamais vers une table de définitions publiée.

**Décision** : les codes sont conservés tels quels dans les données, et marqués `nature_verifie = "non"` dans `data/reference/nature_condition.csv`. Ce champ est traité comme une information secondaire dans l'analyse (jamais comme un résultat central), et aucune signification devinée n'est présentée comme certaine.

## 6. Table de référence des chapitres ATA

Construite à partir de la nomenclature ATA-100 standard, largement documentée dans l'industrie aéronautique (contrairement aux codes `NatureOfCondition`, propres au formulaire FAA). Sur les 46 chapitres présents dans les données : 40 confirmés avec un niveau de confiance élevé, 1 non documenté avec certitude (chapitre 14, rare). Détail dans `data/reference/ata_chapitres.csv`.

## 7. Valeurs aberrantes (âge de l'appareil)

`AircraftTotalCycles` et `AircraftTotalTime` contiennent de rares valeurs extrêmes manifestement erronées (jusqu'à 5,68 millions de cycles pour un seul avion). Ces valeurs sont neutralisées (mises à vide) au-delà d'un seuil de 150 000, plutôt que plafonnées à ce seuil — un plafonnement aurait fait passer une valeur clairement fausse pour une vraie mesure d'avion très âgé, ce qui aurait faussé l'analyse par tranche d'âge. 8 valeurs de cycles et 139 valeurs d'heures ont été neutralisées sur 140 139 lignes.

## 8. Année 2026

2026 est l'année en cours au moment de cette analyse (données de janvier à juillet uniquement). Elle est conservée dans le jeu de données mais marquée `annee_complete = False`, et exclue par défaut de toute comparaison année sur année, pour ne pas comparer une année partielle à des années complètes.

---

*(Section réservée : conclusions et limites propres à chaque bloc d'analyse — cartographie ATA, âge/usure, text mining, tendance temporelle — à compléter au fur et à mesure de leur construction.)*
