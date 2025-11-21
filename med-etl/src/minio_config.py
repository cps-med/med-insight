# -----------------------------------------------------------------------
# minio_config.py
# -----------------------------------------------------------------------
# MinIO S3-compatible storage configuration and utilities
# -----------------------------------------------------------------------

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_minio_s3_options():
    """
    Get MinIO S3 connection options from environment variables.
    
    Returns:
        dict: S3 options dictionary for pandas/pyarrow S3 operations
        
    Raises:
        ValueError: If required MinIO environment variables are not set
    """
    # Validate required environment variables
    required_vars = ['MINIO_ENDPOINT', 'MINIO_ACCESS_KEY', 'MINIO_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required MinIO environment variables: {', '.join(missing_vars)}")
    
    endpoint = os.environ.get('MINIO_ENDPOINT')
    use_ssl = os.environ.get('MINIO_USE_SSL', 'false').lower() == 'true'
    protocol = 'https' if use_ssl else 'http'
    
    return {
        "key": os.environ.get('MINIO_ACCESS_KEY'),
        "secret": os.environ.get('MINIO_SECRET_KEY'),
        "client_kwargs": {
            "endpoint_url": f"{protocol}://{endpoint}"
        }
    }

def get_minio_bucket_name():
    """
    Get MinIO bucket name from environment variables.
    
    Returns:
        str: Bucket name
        
    Raises:
        ValueError: If MINIO_BUCKET_NAME environment variable is not set
    """
    bucket_name = os.environ.get('MINIO_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("MINIO_BUCKET_NAME environment variable is not set")
    
    return bucket_name

def build_s3_path(file_path):
    """
    Build complete S3 path using bucket name from environment and provided file path.
    
    Args:
        file_path (str): Relative file path within the bucket (e.g., "extract-file/lbb/file.parquet")
        
    Returns:
        str: Complete S3 path (e.g., "s3://med-sandbox/extract-file/lbb/file.parquet")
    """
    bucket_name = get_minio_bucket_name()
    return f"s3://{bucket_name}/{file_path.lstrip('/')}"