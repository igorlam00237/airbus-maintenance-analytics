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

## Conclusions par bloc d'analyse

### Bloc 1 — Cartographie ATA

Le volume de signalements est très concentré : le chapitre **Fuselage** représente à lui seul 30% de tous les signalements A320/A330/A350. Les 7 premiers chapitres (Fuselage, Éclairage, Portes, Équipements/aménagements, Climatisation, Empennages, Voilure) totalisent 82% du volume — la règle des 80/20 se vérifie presque exactement.

Le taux normalisé (signalements pour 1000 avions distincts) donne une lecture différente du comptage brut : par exemple, l'A330 a un taux de signalement "Fuselage" nettement plus élevé que l'A320 une fois ramené à sa taille de flotte, alors qu'en comptage brut l'A320 domine largement (parce qu'il y a beaucoup plus d'A320 en service).

**Limite** : les taux normalisés pour l'A330 (210 avions distincts) et surtout l'A350 (41 avions) reposent sur des échantillons bien plus petits que l'A320 (2 568 avions) — donc plus sensibles au bruit statistique.

### Bloc 2 — Âge / usure

Deux profils bien distincts selon l'âge de l'appareil (tranches calculées en terciles **par famille**, pas avec un seuil global — voir la justification dans le notebook 05) :

- **Usure/fatigue** (lift croissant avec l'âge) : Fuselage et surtout Voilure — cohérent avec des éléments structurels soumis à la fatigue mécanique.
- **Défauts de jeunesse** (lift décroissant avec l'âge) : Climatisation, Moteur, Équipements/aménagements, Portes — cohérent avec des systèmes qui posent davantage de problèmes en début de mise en service.

**Limite** : le lift indique une association statistique, pas une preuve de cause. Les tranches d'âge sont relatives à chaque famille — "âgé" ne correspond pas au même nombre de cycles absolu selon la famille.

### Bloc 3 — Text mining

Le texte confirme et **explique** le résultat du bloc 2 : "corrosion" ressort comme terme caractéristique à la fois du Fuselage et de la Voilure — les deux chapitres identifiés comme "usure". Chaque chapitre a un vocabulaire distinct et cohérent (hinge/elevator/stabilizer pour les Empennages, gear/brake/wheel pour le Train d'atterrissage). Résultat le plus surprenant : la Climatisation est dominée par "odor/smell" plutôt que par du vocabulaire mécanique — le problème le plus fréquemment signalé semble être une odeur perçue en cabine plutôt qu'une panne du système en tant que tel.

**Limite** : les 22 codes `NatureOfConditionA` n'ont pas pu être exploités faute de documentation FAA publique (voir §5) — le text mining sur `Discrepancy` reste la source principale d'information qualitative sur la nature des pannes.

### Bloc 4 — Tendance temporelle

La hausse brute du nombre de signalements (×2,5 entre 2015 et 2025) s'explique en grande partie par la croissance de la flotte observée (×1,9 sur la même période) — pas par une dégradation réelle de la fiabilité. Le taux normalisé n'a pas de tendance nette sur 10 ans et atteint son minimum en 2020, vraisemblablement un effet Covid (moins d'avions en vol, donc moins d'occasions de détecter et signaler un problème — une baisse de taux ne signifie pas toujours moins de pannes, elle peut signifier moins d'exposition).

**Limite** : les variations d'une année sur l'autre pour un chapitre donné peuvent être bruyantes sur un seul point de comparaison (2024 → 2025) — à confirmer sur plusieurs années avant de conclure à une tendance structurelle.

---

## Incident corrigé pendant la construction

Le fichier `agg_taille_flotte.parquet` (utilisé pour normaliser les comparaisons) a d'abord été calculé en incluant par erreur l'année 2026 (partielle), à cause d'un filtre manquant dans le notebook de nettoyage. L'erreur a été repérée avant que la moindre conclusion n'en soit tirée (dans le notebook de tendance temporelle, avant rédaction de la synthèse), corrigée à la source, et une assertion explicite a été ajoutée pour détecter une régression future. Un audit des notebooks en amont a confirmé qu'aucun résultat déjà publié n'était affecté. Documenté ici par souci de transparence sur le processus de construction, pas seulement sur le résultat final.
