"""
Utilitaires pour le téléchargement et l'upload de données vers Google Cloud Storage.

Ce module fournit des fonctions pour :
- Télécharger des fichiers Parquet depuis l'API Île-de-France Mobilités
- Uploader des fichiers vers GCS
- Uploader récursivement des dossiers vers GCS
"""

# Standard library imports
from pathlib import Path
from typing import List, Optional

# Third-party imports
import requests
from google.cloud import storage


def download_parquet_from_idfm(
    dataset_name: str,
    data_dir: Path,
    timeout: int = 300
) -> Path:
    """
    Télécharge un fichier Parquet depuis l'API Île-de-France Mobilités.
    
    Args:
        dataset_name: Nom du dataset à télécharger (ex: 'emplacement-des-gares-idf')
        data_dir: Dossier de destination pour le fichier téléchargé
        timeout: Timeout en secondes pour la requête HTTP (défaut: 300)
    
    Returns:
        Path: Chemin vers le fichier Parquet téléchargé
    
    Raises:
        requests.HTTPError: Si la requête HTTP échoue
        FileNotFoundError: Si le dossier de destination ne peut pas être créé
    """
    url = (
        f"https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/"
        f"{dataset_name}/exports/parquet?parquet_compression=snappy"
    )
    output_file = f"{dataset_name}.parquet"
    
    dataset_dir = data_dir / dataset_name
    dataset_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = dataset_dir / output_file
    
    print(f"[...] - Téléchargement du fichier Parquet {dataset_name}...")
    
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    
    parquet_path.write_bytes(response.content)
    
    file_size_mb = parquet_path.stat().st_size / (1024 * 1024)
    print(f"[OK] - Téléchargé: {parquet_path}")
    print(f"[OK] - Taille: {file_size_mb:.2f} MB")
    
    return parquet_path


def upload_to_gcs(
    file_path: Path,
    storage_client: storage.Client,
    bucket_name: str,
    gcs_folder: str = "bronze",
    gcs_subfolder: str = ""
) -> str:
    """
    Upload un fichier local vers Google Cloud Storage.
    
    Args:
        file_path: Chemin vers le fichier local à uploader
        storage_client: Client Google Cloud Storage
        bucket_name: Nom du bucket GCS
        gcs_folder: Dossier de base dans GCS (défaut: "bronze")
        gcs_subfolder: Sous-dossier dans GCS (défaut: "")
    
    Returns:
        str: URI GCS du fichier uploadé (gs://bucket/path)
    
    Raises:
        FileNotFoundError: Si le fichier local n'existe pas
        google.cloud.exceptions.GoogleCloudError: Si l'upload échoue
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    bucket = storage_client.bucket(bucket_name)
    gcs_path = (
        f"{gcs_folder}/{gcs_subfolder}/{file_path.name}"
        if gcs_subfolder
        else f"{gcs_folder}/{file_path.name}"
    )
    blob = bucket.blob(gcs_path)
    
    print(f"[...] - Upload de {file_path.name} vers GCS...")
    blob.upload_from_filename(str(file_path))
    
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    print(f"[OK] - Uploadé: gs://{bucket_name}/{gcs_path}")
    print(f"[OK] - Taille: {file_size_mb:.2f} MB")
    
    return f"gs://{bucket_name}/{gcs_path}"


def upload_folder_to_gcs(
    folder_path: Path,
    storage_client: storage.Client,
    bucket_name: str,
    gcs_folder: str = "bronze",
    gcs_subfolder: str = "",
    extensions: Optional[List[str]] = None
) -> int:
    """
    Upload récursivement tous les fichiers d'un dossier vers GCS en préservant la structure.
    
    Args:
        folder_path: Chemin du dossier local à uploader
        storage_client: Client Google Cloud Storage
        bucket_name: Nom du bucket GCS
        gcs_folder: Dossier de base dans GCS (défaut: "bronze")
        gcs_subfolder: Sous-dossier dans GCS (défaut: "")
        extensions: Liste des extensions à uploader (ex: [".csv", ".txt"]).
                   Si None, upload tous les fichiers
    
    Returns:
        int: Nombre de fichiers uploadés
    
    Raises:
        FileNotFoundError: Si le dossier local n'existe pas
        google.cloud.exceptions.GoogleCloudError: Si l'upload échoue
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        raise FileNotFoundError(f"Le dossier {folder_path} n'existe pas")
    
    # Normaliser les extensions (ajouter le point si absent, mettre en minuscule)
    if extensions:
        extensions = [
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in extensions
        ]
    
    bucket = storage_client.bucket(bucket_name)
    uploaded_files = 0
    total_size = 0
    skipped_files = 0
    
    print(f"[...] - Upload du dossier {folder_path.name} vers GCS...")
    if extensions:
        print(f"[...] - Extensions filtrées: {', '.join(extensions)}")
    
    # Parcourir récursivement tous les fichiers
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            # Filtrer par extension si spécifié
            if extensions and file_path.suffix.lower() not in extensions:
                skipped_files += 1
                continue
            
            # Calculer le chemin relatif depuis le dossier source
            relative_path = file_path.relative_to(folder_path)
            
            # Construire le chemin GCS en préservant la structure
            if gcs_subfolder:
                gcs_path = f"{gcs_folder}/{gcs_subfolder}/{relative_path.as_posix()}"
            else:
                gcs_path = f"{gcs_folder}/{relative_path.as_posix()}"
            
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(str(file_path))
            
            file_size = file_path.stat().st_size
            total_size += file_size
            uploaded_files += 1
            
            print(f"  ✓ {relative_path.as_posix()}")
    
    total_size_mb = total_size / (1024 * 1024)
    print(f"[OK] - {uploaded_files} fichiers uploadés")
    if skipped_files > 0:
        print(f"[OK] - {skipped_files} fichiers ignorés (extension non autorisée)")
    print(f"[OK] - Taille totale: {total_size_mb:.2f} MB")
    print(
        f"[OK] - Dossier GCS: "
        f"gs://{bucket_name}/{gcs_folder}/{gcs_subfolder if gcs_subfolder else folder_path.name}/"
    )
    
    return uploaded_files

