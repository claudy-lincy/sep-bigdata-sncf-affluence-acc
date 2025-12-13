# SEP – Big Data SNCF (ETL + BigQuery) – Silver / Gold

Projet de M2 SEP – Forecast de l’affluence des gares SNCF  
Auteurs : Adama, Claudy et Charifatou(acc)

(Repo inspiré du template fourni par le prof.)


---

## Objectif du projet

L’objectif de ce projet est de construire un pipeline Big Data permettant :
- l’ingestion de données publiques liées au réseau SNCF / Île-de-France Mobilités,
- leur structuration dans BigQuery selon une architecture Bronze / Silver / Gold,
- l’analyse de l’affluence ferroviaire via des indicateurs métier (KPIs),
- et la préparation des données pour des usages analytiques et de prévision.


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
3. **Gold** (BigQuery) : Données Nettoyées, agrégées et optimisées pour l'analyse métier

## Liens vers les Sources de Données

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

## 1) Prérequis

### Outils locaux
- Python 3.10+ (recommandé)
- Git
- VS Code (ou équivalent)
- Jupyter (via `pip` ou VS Code)

### Google Cloud
- Un projet GCP actif (ex: `idfm-etl-reims-0224dy2025dy`)
- BigQuery activé
- Un compte de service (Service Account) avec droits BigQuery + Storage
- Une clé JSON du service account (⚠️ à ne jamais committer)

---

## 2) Cloner le projet

```bash
git clone https://github.com/claudy-lincy/sep-bigdata-sncf-affluence-acc.git
cd sep-bigdata-sncf-affluence-acc


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

### Configuration GCP (liaison “local ↔ cloud”)

Créer un fichier `.env` à la racine du projet :

```env
PROJECT_ID=idfm-etl-reims-0224dy2025dy
GOOGLE_APPLICATION_CREDENTIALS=secrets/your-service-account.json
BUCKET_NAME=your-gcs-bucket-name
```
# Clé JSON du service account

Placer la clé dans :
secrets/<service-account>.json
 Vérifier que secrets/ est bien dans .gitignore (obligatoire).

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
- **Python**
- **Pandas**

### Organisation des couches de données

Silver : tables nettoyées/structurées (dimensions + facts)
Gold : tables orientées métier (KPIs, agrégats, vues finales)

## Important : “Gold dans Silver” (contexte BigQuery)

Dans ce projet, les tables KPI (Gold) peuvent être créées dans le dataset 
silver car BigQuery impose une contrainte stricte de localisation :

Un dataset silver créé automatiquement par notebook peut être en 
multi-région US

L’interface GCP peut ne proposer que des régions (ex: us-east1) pour créer un dataset “gold”

On ne peut pas requêter entre US (multi-région) et us-east1 (erreur de localisation)

# Solution adoptée : matérialisation des tables KPI (Gold) dans le dataset silver pour garantir l’exécution des requêtes.



## Licence

Ce projet est destiné à un usage pédagogique dans le cadre du M2 SEP et M2 CS de l'Université de Reims Champagne-Ardenne.

## Auteurs

Projet réalisé dans le cadre des M2 SEP et M2 CS de l'université de Reims Champagne-Ardenne.
