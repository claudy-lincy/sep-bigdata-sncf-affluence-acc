# Pipeline ETL Big Data - SNCF GCP

Pipeline ETL pour l'analyse des données de transport en commun d'Île-de-France sur Google Cloud Platform.

## Structure du Projet

```
m2-univ-reims-sep-cs-etl-sncf-gcp/
├── notebooks/
│   ├── 0_test_connection.ipynb          # Test de connexion GCS/BigQuery
│   ├── 1_[EXTRACT]_ingest_to_gcs.ipynb    # Extraction et ingestion vers GCS (bronze)
│   ├── 2_[LOAD]_load_to_bigquery.ipynb    # Chargement vers BigQuery (silver)
│   └── 3_[TRANSFORM]_analyze_for_gold.ipynb  # Analyse pour la couche gold
├── src/
│   ├── gcs_utils.py                       # Utilitaires GCS
│   └── bq_utils.py                        # Utilitaires BigQuery
├── data/                                  # Données locales (temporaires)
├── secrets/                               # Credentials GCP
└── requirements.txt                       # Dépendances Python
```

## Architecture du Pipeline

Le pipeline suit une architecture en **3 couches** (Medallion Architecture) :

1. **Bronze** (GCS) : Données brutes, non transformées
2. **Silver** (BigQuery) : Données brutes chargées sur BigQuery
3. **Gold** (BigQuery) : Données Nettoyées et agrégées et optimisées pour l'analyse métier

## Tables de Données

### Tables de Dimension

#### `dim_gare`
- **Description** : Emplacement et informations géographiques de toutes les gares d'Île-de-France
- **Source** : Île-de-France Mobilités
- **Documentation** : [Emplacement des gares IDF](https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/information/)
- **Format** : Parquet
- **Clé primaire** : `id_gares`
- **Colonnes principales** : `id_gares`, `nom_gares`, `geo_point_2d`, `geo_shape`, `idrefliga`, `mode`, `exploitant`

#### `dim_ligne`
- **Description** : Référentiel de toutes les lignes de transport en commun d'Île-de-France
- **Source** : Île-de-France Mobilités
- **Documentation** : [Référentiel des lignes](https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/information/)
- **Format** : Parquet
- **Colonnes principales** : Informations sur les lignes (numéros, noms, types de transport)

#### `dim_arret`
- **Description** : Référentiel de tous les arrêts de transport en commun d'Île-de-France
- **Source** : Île-de-France Mobilités
- **Documentation** : [Arrêts](https://data.iledefrance-mobilites.fr/explore/dataset/arrets/information/)
- **Format** : Parquet
- **Colonnes principales** : Informations sur les arrêts (noms, coordonnées, lignes desservies)

#### `dim_transporteur`
- **Description** : Liste de tous les transporteurs (opérateurs de transport) d'Île-de-France
- **Source** : Île-de-France Mobilités
- **Documentation** : [Liste des transporteurs](https://data.iledefrance-mobilites.fr/explore/dataset/liste-transporteurs/information/)
- **Format** : Parquet
- **Colonnes principales** : Informations sur les transporteurs (noms, codes, types)

#### `dim_vacances_scolaires`
- **Description** : Calendrier des vacances scolaires pour différentes zones et années
- **Source** : Ministère de l'Éducation Nationale
- **Documentation** : [Calendrier scolaire](https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire/information/)
- **Format** : CSV
- **Colonnes principales** : Dates de début/fin de vacances, zones, années

#### `dim_jours_feries`
- **Description** : Liste des jours fériés en France métropolitaine
- **Source** : API Calendrier Gouv
- **Documentation** : [API Jours Fériés](https://calendrier.api.gouv.fr/jours-feries/)
- **Format** : JSON (un fichier par année)
- **Colonnes principales** : Date, nom du jour férié

### Tables de Fait

#### `fact_validations`
- **Description** : Données historiques de validations des titres de transport sur le réseau ferré d'Île-de-France
- **Source** : Île-de-France Mobilités
- **Documentation** : [Validations historiques réseau ferré](https://data.iledefrance-mobilites.fr/explore/dataset/histo-validations-reseau-ferre/information/)
- **Format** : CSV/TXT (format variable selon les années)
- **Période** : 2015-2024
- **Granularité** : Jour × Gare × Catégorie de titre
- **Colonnes principales** : 
  - `JOUR` : Date de validation (format DD/MM/YYYY)
  - `ID_ZDC` / `lda` / `ID_REFA_LDA` : Identifiant de la gare (non normalisé)
  - `CODE_STIF_TRNS` : Code de la ligne
  - `CODE_STIF_ARRET` : Code de l'arrêt
  - `CATEGORIE_TITRE` : Type de titre de transport
  - `NB_VALD` : Nombre de validations

**Note** : Les fichiers ont des formats différents selon les années (encodage, séparateur, noms de colonnes).

## 🔗 Liens vers les Sources de Données

### Île-de-France Mobilités
- **Portail Open Data** : https://data.iledefrance-mobilites.fr/
- **API Documentation** : https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/
- **Datasets utilisés** :
  - [Emplacement des gares](https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/)
  - [Référentiel des lignes](https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/)
  - [Arrêts](https://data.iledefrance-mobilites.fr/explore/dataset/arrets/)
  - [Liste des transporteurs](https://data.iledefrance-mobilites.fr/explore/dataset/liste-transporteurs/)
  - [Validations historiques réseau ferré](https://data.iledefrance-mobilites.fr/explore/dataset/histo-validations-reseau-ferre/)

### Ministère de l'Éducation Nationale
- **Portail Open Data** : https://data.education.gouv.fr/
- **Dataset** : [Calendrier scolaire](https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire/)

### API Calendrier Gouv
- **Documentation** : https://calendrier.api.gouv.fr/
- **Endpoint Jours Fériés** : https://calendrier.api.gouv.fr/jours-feries/

### Open-Meteo
- **Documentation** : https://open-meteo.com/en/docs
- **API Historique** : https://open-meteo.com/en/docs/historical-weather-api

### GeoAPI
- **Documentation** : https://geo.api.gouv.fr/
- **API Communes** : https://geo.api.gouv.fr/communes

## Démarrage Rapide

### Prérequis

1. **Compte Google Cloud Platform** avec un projet créé
2. **Service Account** avec les permissions nécessaires
3. **Bucket GCS** créé
4. **Python 3.11+** avec les packages installés

### Installation

```bash
# Cloner le repository
git clone <repository-url>
cd m2-univ-reims-sep-cs-etl-sncf-gcp

# Installer les dépendances
pip install -r requirements.txt

```

### Configuration

Créer un fichier `.env` à la racine du projet :

```env
PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=secrets/your-service-account.json
BUCKET_NAME=your-gcs-bucket-name
```

### Exécution des Notebooks

1. **Notebook 0** : Tester la connexion à GCS et BigQuery
2. **Notebook 1** : Extraire et ingérer les données vers GCS (bronze)
3. **Notebook 2** : Charger les données vers BigQuery (silver)
4. **Notebook 3** : Analyser les données pour préparer la couche gold

## Documentation des Notebooks

- **`0_test_connection.ipynb`** : Vérification de la configuration et des connexions
- **`1_[EXTRACT]_ingest_to_gcs.ipynb`** : Extraction depuis les APIs publiques et ingestion vers GCS
- **`2_[LOAD]_load_to_bigquery.ipynb`** : Chargement des données depuis GCS vers BigQuery avec schéma en étoile
- **`3_[TRANSFORM]_analyze_for_gold.ipynb`** : Analyse des données pour identifier les transformations nécessaires à la couche gold

## Technologies Utilisées
- **Google Cloud Python SDK** : Interaction avec les services GCP
- **Google Cloud Storage (GCS)** : Stockage des données brutes
- **BigQuery** : Data warehouse pour l'analyse
- **Python** : Langage de programmation
- **Pandas** : Manipulation de données (inspection locale uniquement)


## 📝 Licence

Ce projet est destiné à un usage pédagogique dans le cadre du Master 2 de l'Université de Reims.

## 👥 Auteurs

Projet réalisé dans le cadre du Master 2 - Université de Reims Champagne-Ardenne.
