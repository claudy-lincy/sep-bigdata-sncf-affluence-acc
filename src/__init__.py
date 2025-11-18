"""
Package src - Utilitaires pour le pipeline ETL GCP.
"""

from .bq_utils import (
    load_csv_from_gcs,
    load_parquet_from_gcs,
)
from .gcs_utils import (
    download_parquet_from_idfm,
    upload_folder_to_gcs,
    upload_to_gcs,
)

__all__ = [
    # GCS utilities
    "download_parquet_from_idfm",
    "upload_to_gcs",
    "upload_folder_to_gcs",
    # BigQuery utilities
    "load_parquet_from_gcs",
    "load_csv_from_gcs",
]

