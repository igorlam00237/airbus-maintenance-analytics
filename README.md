# Airbus Maintenance Analytics

Cartographie des défaillances de maintenance non programmée sur la flotte Airbus actuelle (A320 / A330 / A350), à partir des rapports publics de la FAA (Federal Aviation Administration) : par système d'appareil (chapitre ATA), par âge de flotte, et par motifs récurrents dans les narratifs techniques.

> **Statut du projet** : en cours de construction. Ce README est mis à jour au fur et à mesure — les sections marquées *(à venir)* correspondent à des analyses pas encore construites.

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
├── src/sdr_analytics/    Fonctions partagées (classification, nettoyage, métriques)
├── notebooks/            Un notebook par étape de l'analyse
├── tests/                 Tests automatiques
├── dashboard/             Application Streamlit (à venir)
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
- [ ] Cartographie des défaillances par chapitre ATA *(à venir)*
- [ ] Analyse âge de l'appareil vs profil de pannes *(à venir)*
- [ ] Analyse des narratifs techniques (text mining) *(à venir)*
- [ ] Tendance temporelle par chapitre ATA *(à venir)*
- [ ] Dashboard Streamlit *(à venir)*

## Méthodologie et limites

Voir [`docs/methodologie_limites.md`](docs/methodologie_limites.md) pour le détail des choix méthodologiques et de leurs limites (biais géographique, biais du signalement événementiel, échantillon réduit pour certaines familles, statut des codes non vérifiés, etc.).
