# med-ml

AI and Machine learning layer for Med-Insight

## Overview

**med-ml** is the artificial intelligence and machine learning engine of the Med-Insight application. It transforms cleaned and structured clinical data into predictive models, risk assessments, and data-driven insights using a traditional data science workflow with JupyterLab notebooks.

### Technology Stack

- **Python 3.11** - Core language
- **JupyterLab** - Interactive notebook environment
- **Pandas & NumPy** - Data manipulation
- **PyArrow** - Parquet file handling
- **scikit-learn** - Machine learning algorithms
- **MinIO** - S3-compatible object storage (via boto3 + s3fs)

## Project Structure

```
med-ml/
├── src/                           # All code (notebooks + Python modules)
│   ├── config.py                  # Centralized configuration
│   ├── ddi_transforms.py          # DDI-specific transformations
│   ├── 01_dataprep.ipynb          # Data preparation
│   ├── 02_explore.ipynb           # Exploratory data analysis
│   ├── 03_clean.ipynb             # Data cleaning
│   ├── 04_features.ipynb          # Feature engineering
│   ├── 05_models.ipynb            # Model development
│   └── 06_analysis.ipynb          # Results analysis
└── README.md                      # This file
```

## Medallion Architecture

Data processing follows a versioned medallion architecture stored in MinIO:

| Tier | Prefix | Description | Location |
|------|--------|-------------|----------|
| **Raw** | `v1_raw` | Unmodified source data (Parquet) | `med-data/v1_raw/ddi/` |
| **Clean** | `v2_clean` | Cleaned and validated data | `med-data/v2_clean/ddi/` |
| **Features** | `v3_features` | Feature-engineered datasets | `med-data/v3_features/ddi/` |
| **Models** | `v4_models` | Model outputs and predictions | `med-data/v4_models/ddi/` |

**Source data** resides in: `med-sandbox/kaggle-data/ddi/`

## Setup

### Prerequisites

Ensure you've completed the shared infrastructure setup from **med-data**:
- ✅ Docker Desktop running
- ✅ MinIO container (`med-insight-minio`) running
- ✅ Python 3.11 installed
- ✅ Root `.env` file configured

### Install ML Dependencies

```bash
cd ~/swdev/med/med-insight
source .venv/bin/activate

# Install Jupyter and ML packages
pip install jupyterlab ipykernel notebook matplotlib seaborn scikit-learn

# Update requirements
pip freeze > requirements.txt
```

### Prepare Source Data

1. Upload source CSV to MinIO:
   - Access MinIO Console: http://localhost:9001
   - Navigate to bucket: `med-sandbox`
   - Create folder path: `kaggle-data/ddi/`
   - Upload: `db_drug_interactions.csv`

2. Create destination bucket structure:
   - Bucket: `med-data` (create if doesn't exist)
   - Create folders: `v1_raw/ddi/`, `v2_clean/ddi/`, `v3_features/ddi/`, `v4_models/ddi/`

## Running Notebooks

### Using VS Code (Recommended)

1. Open project in VS Code
2. Navigate to: `med-ml/src/`
3. Open notebook: `01_dataprep.ipynb`
4. Select kernel: `.venv` (Python 3.11)
5. Run cells interactively

### Using JupyterLab

```bash
cd ~/swdev/med/med-insight/med-ml/src
source ../../.venv/bin/activate
jupyter lab
```

Access at: http://localhost:8888

## Workflow

### 1. Data Preparation (`01_dataprep.ipynb`)
- Read CSV from `med-sandbox/kaggle-data/ddi/`
- Write unmodified Parquet to `med-data/v1_raw/ddi/`
- Verify data integrity

### 2. Exploratory Data Analysis (`02_explore.ipynb`)
- Load from v1_raw
- Examine schema, distributions, missing values
- Identify data quality issues

### 3. Data Cleaning (`03_clean.ipynb`)
- Apply transformations from `ddi_transforms.py`
- Handle missing values, duplicates
- Write to v2_clean

### 4. Feature Engineering (`04_features.ipynb`)
- Create risk scoring features
- Encode categorical variables
- Write to v3_features

### 5. Model Development (`05_models.ipynb`)
- Train risk prediction models
- Hyperparameter tuning
- Write outputs to v4_models

### 6. Analysis (`06_analysis.ipynb`)
- Evaluate model performance
- Generate insights and reports

## Configuration

All configuration is centralized in `src/config.py`:

```python
# MinIO settings (loaded from root .env)
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "<from .env>"

# Buckets
SOURCE_BUCKET = "med-sandbox"
DEST_BUCKET = "med-data"

# Data paths
SOURCE_DDI_PATH = "kaggle-data/ddi/"
V1_RAW_PREFIX = "v1_raw/ddi/"
V2_CLEAN_PREFIX = "v2_clean/ddi/"
V3_FEATURES_PREFIX = "v3_features/ddi/"
V4_MODELS_PREFIX = "v4_models/ddi/"
```

## Use Case: Drug-Drug Interaction (DDI) Risk Analysis

The initial use case identifies DDI risks from patient prescription data:

1. **Input**: DDI reference dataset (`db_drug_interactions.csv`)
2. **Goal**: Risk identification and scoring for patient prescriptions
3. **Output**: Risk scores and recommendations for clinical decision support

## Development Notes

- Notebooks use standard Python logging (info level) to stdout
- Follow test-then-batch pattern: test with small samples before full processing
- Track metrics: row counts, processing time, data quality
- All imports use: `from config import *` for consistency

## Next Steps

1. Run `01_dataprep.ipynb` to convert source CSV to Parquet
2. Create `02_explore.ipynb` for EDA after examining data schema
3. Implement cleaning logic in `ddi_transforms.py` based on findings
4. Develop feature engineering and risk scoring models

## Additional Resources

- **MinIO Console**: http://localhost:9001 (login with credentials from .env)
- **Root .env**: `/Users/chuck/swdev/med/med-insight/.env` (shared configuration)
