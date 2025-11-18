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
git clone https://github.com/ettouilebouael/m2-univ-reims-sep-cs-etl-sncf-gcp
cd m2-univ-reims-sep-cs-etl-sncf-gcp

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

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


## Licence

Ce projet est destiné à un usage pédagogique dans le cadre du Master 2 de l'Université de Reims.

## Auteurs

Projet réalisé dans le cadre du Master 2 - Université de Reims Champagne-Ardenne.
