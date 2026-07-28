# Airbus Maintenance Analytics

Cartographie des défaillances de maintenance non programmée sur la flotte Airbus actuelle (A320 / A330 / A350), à partir des rapports publics de la FAA (Federal Aviation Administration) : par système d'appareil (chapitre ATA), par âge de flotte, et par motifs récurrents dans les narratifs techniques.

**[▶ Voir le dashboard en ligne](https://airbus-maintenance-analytics-igorlaminsi.streamlit.app/)** · [Code source](https://github.com/igorlam00237/airbus-maintenance-analytics)

## Résultats clés

- **Le volume de signalements est très concentré** : un seul chapitre (Fuselage) représente 30% de tous les signalements. 7 chapitres sur 46 (Fuselage, Éclairage, Portes, Équipements, Climatisation, Empennages, Voilure) totalisent 82% du volume.
- **La hausse brute du nombre de signalements dans le temps (×2,5 entre 2015 et 2025) s'explique en grande partie par la croissance de la flotte** (×1,9 sur la même période) — le taux normalisé, lui, n'a pas de tendance nette. 2020 (Covid) se démarque comme le creux le plus net.
- **Deux profils de pannes distincts selon l'âge de l'appareil** : usure/fatigue pour les chapitres structurels (Fuselage, Voilure — plus signalés sur les avions âgés) vs défauts de jeunesse pour les systèmes/équipements (Climatisation, Moteur, Portes — plus signalés sur les avions jeunes).
- **Le text mining confirme et explique ce second point** : "corrosion" ressort comme terme caractéristique du Fuselage et de la Voilure — cohérent avec un phénomène qui s'accumule avec les cycles de vol. La Climatisation, elle, est dominée par des signalements d'odeur ("odor/smell") plutôt que par des pannes mécaniques classiques.

Détail complet de chaque analyse : voir les notebooks dans `notebooks/`, ou le dashboard interactif.

## Source des données

[FAA Service Difficulty Reports (SDR)](https://www.faa.gov/av-info/download_SDR) — rapports de dysfonctionnements, pannes ou défauts constatés sur des aéronefs, transmis à la FAA par les compagnies aériennes et ateliers de maintenance. Un fichier par année (2015-2026 utilisés ici).

**Biais assumé dès le départ** : ces données couvrent les appareils exploités par des opérateurs *américains*. Les résultats de ce projet sont un proxy sur la flotte Airbus opérée aux États-Unis, pas une vision de la flotte mondiale.

## Périmètre de l'analyse

Familles retenues : **A320** (inclut A318/A319/A320/A321), **A330**, **A350** — la flotte Airbus actuellement produite et commercialisée.

Familles explicitement exclues, avec leur raison :

| Famille | Raison de l'exclusion |
|---|---|
| A300 / A310 | Générations antérieures, production arrêtée depuis longtemps (2007 / 1998) |
| A340 | Génération de l'A330, production arrêtée ~2011 |
| A380 | Production arrêtée en 2021, échantillon négligeable dans les données |
| A220 | Conception d'origine Bombardier, pas une ingénierie Airbus native |
| Hélicoptères (Airbus Helicopters) | Catégorie d'appareil différente, pas des avions de ligne |

Le détail chiffré de ces exclusions est dans [`docs/methodologie_limites.md`](docs/methodologie_limites.md).

## Structure du projet

```
airbus-maintenance-analytics/
├── data/
│   ├── raw/            Données brutes FAA (non versionnées, à télécharger — voir plus bas)
│   ├── reference/       Tables de référence (chapitres ATA, codes de condition)
│   └── processed/       Données nettoyées, prêtes à l'analyse
├── src/sdr_analytics/    Fonctions partagées (classification, nettoyage, métriques, texte)
├── notebooks/            Un notebook par étape de l'analyse (01 à 06)
├── tests/                 Tests automatiques
├── dashboard/             Application Streamlit (accueil + 4 pages d'analyse)
└── docs/                  Méthodologie et limites détaillées
```

## Reproduire l'analyse

```bash
git clone git@github.com:igorlam00237/airbus-maintenance-analytics.git
cd airbus-maintenance-analytics
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Les données brutes ne sont pas incluses dans le dépôt (volumineuses, ~320 Mo). Télécharger les fichiers CSV par année depuis la [page FAA](https://www.faa.gov/av-info/download_SDR) et les placer dans `data/raw/` sous le nom `SDR-AAAA.csv`.

Puis exécuter les notebooks dans l'ordre (`notebooks/01_...` à `notebooks/06_...`), ou lancer directement le dashboard une fois les données préparées :

```bash
.venv/bin/streamlit run dashboard/app.py
```

## Avancement

- [x] Exploration initiale des données
- [x] Nettoyage, classification par famille, préparation du jeu de données
- [x] Cartographie des défaillances par chapitre ATA
- [x] Analyse âge de l'appareil vs profil de pannes
- [x] Analyse des narratifs techniques (text mining)
- [x] Tendance temporelle par chapitre ATA
- [x] Dashboard Streamlit (4 pages + accueil)
- [x] Déploiement public sur Streamlit Community Cloud

## Méthodologie et limites

Voir [`docs/methodologie_limites.md`](docs/methodologie_limites.md) pour le détail des choix méthodologiques et de leurs limites (biais géographique, biais du signalement événementiel, échantillon réduit pour certaines familles, statut des codes non vérifiés, etc.).
