# Med-ML Pipeline Execution Guide (Option C: Concurrent Care)

**Complete step-by-step guide for executing the full med-ml pipeline with PhysioNet MIMIC-IV concurrent care integration**

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pipeline Overview](#pipeline-overview)
3. [Execution Steps](#execution-steps)
4. [Expected Outputs](#expected-outputs)
5. [Troubleshooting](#troubleshooting)
6. [Validation Checkpoints](#validation-checkpoints)

---

## Prerequisites

### ✅ Infrastructure Requirements

Verify the following are running and accessible:

```bash
# 1. Check Docker containers are running
docker ps

# Should show:
# - sqlserver2019 (SQL Server 2019)
# - med-insight-minio (MinIO object storage)

# If not running, start them:
docker start sqlserver2019 med-insight-minio

# 2. Verify MinIO Console accessible
open http://localhost:9001
# Login with credentials from .env file

# 3. Verify SQL Server accessible
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT @@VERSION"
```

### ✅ Data Prerequisites

Ensure the following data sources are in place:

**CDWWork Database (VA Source Data)**:
```bash
# Verify CDWWork database has all patient data
sqlcmd -S 127.0.0.1,1433 -U sa -P "$CDWWORK_DB_PASSWORD" -d CDWWork -Q "SELECT COUNT(*) AS PatientCount FROM SPatient.SPatient"

# Should show 25 patients (10 base + 5 elderly + 10 expansion)
```

**MinIO Buckets**:
- `med-sandbox` - Raw external data (Kaggle DDI, MIMIC-IV CSVs)
- `med-data` - Processed ML data (Parquet files in medallion architecture)

**MIMIC-IV Demo Data in MinIO**:
```bash
# Verify MIMIC CSV files uploaded to med-sandbox
# Should be in: med-sandbox/mimic-data/hosp/

# Files expected:
# - prescriptions.csv
# - pharmacy.csv
# - emar.csv
# - patients.csv
# - admissions.csv
```

### ✅ Python Environment

```bash
# Navigate to med-ml directory
cd ~/swdev/med/med-insight/med-ml

# Activate virtual environment
source ../.venv/bin/activate

# Verify Python version (should be 3.11.x)
python --version

# Verify key dependencies installed
python -c "import pandas, s3fs, pyarrow, pyodbc; print('Dependencies OK')"
```

---

## Pipeline Overview

### Phase 1: Data Preparation (Notebooks 01a-01d + mimic_patient_selection)

**Purpose**: Load raw data from external sources, convert to Parquet, integrate community care

| Notebook | Input | Output | Duration |
|----------|-------|--------|----------|
| `01a_dataprep_ddi.ipynb` | Kaggle DDI CSV | v1_raw/ddi/*.parquet | ~30 sec |
| `01b_dataprep_medications.ipynb` | CDWWork RxOut, BCMA | v1_raw/medications/*.parquet | ~1 min |
| `01c_dataprep_demographics.ipynb` | CDWWork SPatient | v1_raw/demographics/*.parquet | ~30 sec |
| `01d_dataprep_mimic.ipynb` | MIMIC-IV CSVs | v1_raw/mimic/*.parquet | ~1 min |
| `mimic_patient_selection.ipynb` | v1_raw/mimic/ + v1_raw/medications/ | v1_raw/medications/*.parquet (updated) | ~1 min |

### Phase 2: Analysis Pipeline (Notebooks 02-06)

**Purpose**: Explore, clean, engineer features, cluster, and analyze

| Notebook | Input | Output | Duration |
|----------|-------|--------|----------|
| `02_explore.ipynb` | v1_raw/* | Exploratory analysis | ~2 min |
| `03_clean.ipynb` | v1_raw/* | v2_clean/* | ~2 min |
| `04_features.ipynb` | v2_clean/* | v3_features/* | ~3 min |
| `05_clustering.ipynb` | v3_features/* | v4_models/clusters | ~3 min |
| `06_analysis.ipynb` | v4_models/* | Final insights | ~2 min |

**Total Estimated Time**: 15-20 minutes for complete pipeline

---

## Execution Steps

### Step 1: Activate Environment

```bash
# Navigate to med-ml source directory
cd ~/swdev/med/med-insight/med-ml/src

# Activate Python virtual environment
source ../../.venv/bin/activate

# Verify activation (prompt should show (.venv))
which python
# Should output: /Users/chuck/swdev/med/med-insight/.venv/bin/python
```

### Step 2: Run Phase 1 - Data Preparation

#### 2a. Prepare DDI Reference Data

```bash
# Run 01a_dataprep_ddi.ipynb
jupyter nbconvert --to notebook --execute 01a_dataprep_ddi.ipynb
```

**Expected Output**:
- ✅ "Successfully wrote 191,541 rows"
- ✅ "Verification successful - row counts match"
- Creates: `med-data/v1_raw/ddi/db_drug_interactions.parquet`

**Checkpoint**: Verify file exists in MinIO Console → med-data → v1_raw → ddi/

---

#### 2b. Prepare VA Medication Data

```bash
# Run 01b_dataprep_medications.ipynb
jupyter nbconvert --to notebook --execute 01b_dataprep_medications.ipynb
```

**Expected Output**:
- ✅ "Extracted X medication records from RxOut"
- ✅ "Extracted Y medication administrations from BCMA"
- ✅ "Combined dataset: Z total records"
- Creates: `med-data/v1_raw/medications/patient_medications.parquet`

**Note**: This creates VA-only medications. Will be replaced after MIMIC integration.

---

#### 2c. Prepare Patient Demographics

```bash
# Run 01c_dataprep_demographics.ipynb
jupyter nbconvert --to notebook --execute 01c_dataprep_demographics.ipynb
```

**Expected Output**:
- ✅ "Extracted 25 patient demographic records"
- ✅ "Age distribution: 28-82 years"
- Creates: `med-data/v1_raw/demographics/patient_demographics.parquet`

---

#### 2d. Prepare MIMIC-IV Data

```bash
# Run 01d_dataprep_mimic.ipynb
jupyter nbconvert --to notebook --execute 01d_dataprep_mimic.ipynb
```

**Expected Output**:
- ✅ "Loaded X prescriptions"
- ✅ "Loaded Y patients"
- ✅ "All 5 Parquet files written"
- ✅ "Storage savings: ~85-90% compression"
- Creates: `med-data/v1_raw/mimic/*.parquet` (5 files)

**Checkpoint**: Verify files in MinIO Console → med-data → v1_raw → mimic/

---

#### 2e. Integrate Community Care (Option C: Concurrent)

⚠️ **IMPORTANT**: Before running this notebook, you must update patient mapping!

**Required Action**: Open `mimic_patient_selection.ipynb` and update MIMICSubjectID values

```python
# In Cell 4 of mimic_patient_selection.ipynb, update this section:
patient_mapping = pd.DataFrame([
    {'VAPatientSID': 1011, 'MIMICSubjectID': '[TBD]', ...},  # ← Update [TBD]
    {'VAPatientSID': 1012, 'MIMICSubjectID': '[TBD]', ...},  # ← Update [TBD]
    # ... etc for all 10 patients
])
```

**How to find MIMIC subject IDs**:
1. Run the exploration cell in `mimic_patient_selection.ipynb` (Cell 3)
2. It displays MIMIC patients with prescription counts
3. Select 10 MIMIC subject_ids with 5-15 prescriptions each
4. Update the patient_mapping DataFrame with these IDs

**Option**: For quick testing, the notebook will use demo patients if [TBD] values remain

**Execute the notebook**:
```bash
# Option 1: Interactive (recommended for first run)
jupyter lab mimic_patient_selection.ipynb
# Run cells sequentially, verify mapping, then execute all

# Option 2: Batch execution (after mapping verified)
jupyter nbconvert --to notebook --execute mimic_patient_selection.ipynb
```

**Expected Output**:
- ✅ "Selected X prescriptions for mapped patients"
- ✅ "Transformed dates to 2025 for concurrent care"
- ✅ "Created Y community care medication records"
- ✅ "✅ VALIDATION PASSED: Option C (Concurrent Care) successfully implemented"
- ✅ "All patients have overlapping VA and community medications in 2025"
- Updates: `med-data/v1_raw/medications/patient_medications.parquet` (now includes community care)

**Critical Checkpoint**: Verify concurrent care validation passes!

---

### Step 3: Run Phase 2 - Analysis Pipeline

Now that all data is prepared (including concurrent community care), run the analysis notebooks.

#### 3a. Exploratory Data Analysis

```bash
# Run 02_explore.ipynb
jupyter nbconvert --to notebook --execute 02_explore.ipynb
```

**Expected Output**:
- ✅ "Source System Distribution:"
  - RxOut: X records
  - BCMA: Y records
  - **MIMIC-Community: Z records** ← Should see 3 sources!
- ✅ "Patients with community care: 10"
- ✅ Shows temporal overlap for concurrent care patients

**Checkpoint**: Verify 3 source systems present (not just 2!)

---

#### 3b. Data Cleaning

```bash
# Run 03_clean.ipynb
jupyter nbconvert --to notebook --execute 03_clean.ipynb
```

**Expected Output**:
- ✅ "Cleaning medications data..."
- ✅ "Cleaned dataset: X records"
- Creates: `med-data/v2_clean/medications/*.parquet`

---

#### 3c. Feature Engineering

```bash
# Run 04_features.ipynb
jupyter nbconvert --to notebook --execute 04_features.ipynb
```

**Expected Output**:
- ✅ "Engineered 19 patient-level features"
- ✅ "Created DDI risk features"
- ✅ "Feature matrix: 25 patients × 19 features"
- Creates: `med-data/v3_features/patient_features.parquet`

**Note**: Features now include concurrent care patterns!

---

#### 3d. Patient Risk Clustering

```bash
# Run 05_clustering.ipynb
jupyter nbconvert --to notebook --execute 05_clustering.ipynb
```

**Expected Output**:
- ✅ "Optimal clusters: K"
- ✅ "Silhouette score: X.XX"
- ✅ "Cluster assignments for 25 patients"
- Creates: `med-data/v4_models/clustering_results.parquet`

**Note**: Clustering should reflect dual-source medication patterns for patients with concurrent care.

---

#### 3e. Results Analysis

```bash
# Run 06_analysis.ipynb
jupyter nbconvert --to notebook --execute 06_analysis.ipynb
```

**Expected Output**:
- ✅ "Cluster characteristics analysis"
- ✅ "DDI risk stratification"
- ✅ **"Concurrent care DDI analysis"** ← Key for Option C
- ✅ "Care coordination opportunities identified"

**Key Focus**: Look for DDIs spanning VA and community care ("Blind Spot" scenarios)

---

## Expected Outputs

### MinIO Data Structure (After Complete Pipeline)

```
med-sandbox/
├── kaggle-data/ddi/
│   └── db_drug_interactions.csv
└── mimic-data/hosp/
    ├── prescriptions.csv
    ├── pharmacy.csv
    ├── emar.csv
    ├── patients.csv
    └── admissions.csv

med-data/
├── v1_raw/
│   ├── ddi/
│   │   └── db_drug_interactions.parquet
│   ├── medications/
│   │   └── patient_medications.parquet (VA + MIMIC-Community combined)
│   ├── demographics/
│   │   └── patient_demographics.parquet
│   └── mimic/
│       ├── prescriptions.parquet
│       ├── pharmacy.parquet
│       ├── emar.parquet
│       ├── patients.parquet
│       └── admissions.parquet
├── v2_clean/
│   └── medications/
│       └── patient_medications_clean.parquet
├── v3_features/
│   └── patient_features.parquet
└── v4_models/
    └── clustering_results.parquet
```

### Key Metrics (Expected Values)

| Metric | Expected Value | Notes |
|--------|---------------|-------|
| Total patients | 25 | 10 base + 5 elderly + 10 expansion |
| Patients with community care | 10 | Selected for concurrent care |
| VA medication records | ~60-80 | RxOut + BCMA |
| Community care records | ~40-60 | MIMIC-Community |
| Total medication records | ~100-140 | Combined |
| DDI reference interactions | 191,541 | Kaggle DDI dataset |
| Patient features engineered | 19 | From 04_features.ipynb |
| Source systems | 3 | RxOut, BCMA, MIMIC-Community |

---

## Troubleshooting

### Issue 1: MinIO Connection Errors

**Symptoms**: `EndpointConnectionError`, timeout errors

**Solution**:
```bash
# Verify MinIO running
docker ps | grep minio

# Restart if needed
docker restart med-insight-minio

# Check logs
docker logs med-insight-minio

# Test connectivity
open http://localhost:9001
```

---

### Issue 2: SQL Server Connection Errors

**Symptoms**: `pyodbc.Error`, "Cannot open database"

**Solution**:
```bash
# Verify SQL Server running
docker ps | grep sqlserver

# Restart if needed
docker restart sqlserver2019

# Test connection
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT @@VERSION"

# Verify CDWWork database exists
sqlcmd -S 127.0.0.1,1433 -U sa -P "$CDWWORK_DB_PASSWORD" -Q "SELECT name FROM sys.databases"
```

---

### Issue 3: Missing MIMIC CSV Files

**Symptoms**: `FileNotFoundError` in 01d_dataprep_mimic.ipynb

**Solution**:
```bash
# Verify files uploaded to MinIO
# Open MinIO Console: http://localhost:9001
# Navigate to: med-sandbox → mimic-data → hosp/
# Should see 5 CSV files

# If missing, re-upload from local directory
cd ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp
# Upload via MinIO Console or mc CLI
```

---

### Issue 4: Patient Mapping [TBD] Values

**Symptoms**: Warning in `mimic_patient_selection.ipynb` about placeholder values

**Solution**:
```python
# Open mimic_patient_selection.ipynb in Jupyter
# Run Cell 3 (MIMIC patient exploration)
# Note top 10 MIMIC subject_ids with 5-15 prescriptions
# Update Cell 4 patient_mapping with actual IDs

# Example:
patient_mapping = pd.DataFrame([
    {'VAPatientSID': 1011, 'MIMICSubjectID': 10000032, ...},  # ← Updated
    {'VAPatientSID': 1012, 'MIMICSubjectID': 10000045, ...},  # ← Updated
    # ...
])

# Then re-run the notebook
```

---

### Issue 5: Concurrent Care Validation Fails

**Symptoms**: "NO OVERLAP (sequential, not concurrent)" warnings

**Solution**:
1. Check date transformation logic in `mimic_patient_selection.ipynb`
2. Verify `shift_date_to_2025_concurrent()` using 2025 (not 2024)
3. Verify patient_offsets being applied
4. Check VA medication dates in CDWWork:
   ```sql
   SELECT PatientSID, MIN(IssueDateTime), MAX(IssueDateTime)
   FROM RxOut.RxOutpat
   WHERE PatientSID IN (1011, 1012, 1013, 1014, 1015, 1016, 1019, 1021, 1023, 1024)
   GROUP BY PatientSID;
   ```
5. Ensure both VA and community dates in 2025

---

### Issue 6: Only 2 Source Systems (Missing MIMIC-Community)

**Symptoms**: `02_explore.ipynb` shows only RxOut and BCMA

**Solution**:
```python
# This means mimic_patient_selection.ipynb didn't write successfully
# or wasn't run at all

# Solution:
# 1. Re-run mimic_patient_selection.ipynb
# 2. Verify last cell shows: "✅ Community care integration complete!"
# 3. Check MinIO med-data/v1_raw/medications/patient_medications.parquet
#    file timestamp (should be recent)
# 4. Re-run 02_explore.ipynb
```

---

### Issue 7: Notebook Execution Fails Mid-Pipeline

**Symptoms**: Notebook stops with exception

**Solution**:
```bash
# Run notebook interactively to see detailed error
jupyter lab 01a_dataprep_ddi.ipynb  # (or whichever failed)

# Run cells one by one, check outputs
# Common issues:
# - Missing .env variables (check .env file)
# - Docker containers stopped (restart docker)
# - MinIO bucket doesn't exist (create in Console)
# - Python dependencies missing (pip install -r requirements.txt)
```

---

## Validation Checkpoints

Use these checkpoints to verify pipeline health at each stage:

### ✅ Checkpoint 1: After 01a-01c (Before MIMIC Integration)

```python
# Run this validation in Python/notebook:
import s3fs
from config import *

s3 = s3fs.S3FileSystem(
    anon=False, key=MINIO_ACCESS_KEY, secret=MINIO_SECRET_KEY,
    client_kwargs={'endpoint_url': f"http://{MINIO_ENDPOINT}"}
)

# Check v1_raw files exist
assert s3.exists(f"{DEST_BUCKET}/v1_raw/ddi/db_drug_interactions.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/medications/patient_medications.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/demographics/patient_demographics.parquet")

print("✅ Checkpoint 1 passed: All Phase 1a-1c data prepared")
```

---

### ✅ Checkpoint 2: After 01d (MIMIC Parquet Created)

```python
# Verify MIMIC Parquet files
assert s3.exists(f"{DEST_BUCKET}/v1_raw/mimic/prescriptions.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/mimic/pharmacy.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/mimic/emar.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/mimic/patients.parquet")
assert s3.exists(f"{DEST_BUCKET}/v1_raw/mimic/admissions.parquet")

print("✅ Checkpoint 2 passed: MIMIC data converted to Parquet")
```

---

### ✅ Checkpoint 3: After mimic_patient_selection (Concurrent Care Integrated)

```python
import pandas as pd

# Load combined medications
with s3.open(f"{DEST_BUCKET}/v1_raw/medications/patient_medications.parquet", 'rb') as f:
    df = pd.read_parquet(f)

# Verify 3 source systems
sources = df['SourceSystem'].unique()
assert len(sources) == 3, f"Expected 3 sources, got {len(sources)}: {sources}"
assert 'RxOut' in sources
assert 'BCMA' in sources
assert 'MIMIC-Community' in sources

# Verify community care patients
community_patients = df[df['SourceSystem'] == 'MIMIC-Community']['PatientSID'].nunique()
assert community_patients == 10, f"Expected 10 community care patients, got {community_patients}"

print(f"✅ Checkpoint 3 passed: Concurrent care integrated")
print(f"   - Total medications: {len(df):,}")
print(f"   - Source distribution:")
for source, count in df['SourceSystem'].value_counts().items():
    print(f"     {source}: {count:,}")
```

---

### ✅ Checkpoint 4: After 02-06 (Complete Pipeline)

```python
# Verify all outputs created
assert s3.exists(f"{DEST_BUCKET}/v2_clean/medications/patient_medications_clean.parquet")
assert s3.exists(f"{DEST_BUCKET}/v3_features/patient_features.parquet")
assert s3.exists(f"{DEST_BUCKET}/v4_models/clustering_results.parquet")

print("✅ Checkpoint 4 passed: Complete pipeline executed successfully")
print("\n📊 Pipeline complete! Review 06_analysis.ipynb for insights.")
print("🎯 Key focus: Look for concurrent DDI scenarios spanning VA and community care")
```

---

## Quick Reference Commands

### Start Development Session
```bash
# Start Docker containers
docker start sqlserver2019 med-insight-minio

# Navigate and activate environment
cd ~/swdev/med/med-insight/med-ml/src
source ../../.venv/bin/activate

# Launch Jupyter
jupyter lab
```

### Run Complete Pipeline (Batch)
```bash
# After verifying prerequisites and updating patient mapping
cd ~/swdev/med/med-insight/med-ml/src
source ../../.venv/bin/activate

# Phase 1: Data Preparation
jupyter nbconvert --to notebook --execute 01a_dataprep_ddi.ipynb
jupyter nbconvert --to notebook --execute 01b_dataprep_medications.ipynb
jupyter nbconvert --to notebook --execute 01c_dataprep_demographics.ipynb
jupyter nbconvert --to notebook --execute 01d_dataprep_mimic.ipynb

# Phase 1e: Community Care Integration (interactive recommended)
jupyter lab mimic_patient_selection.ipynb
# Update patient mapping, then execute all cells

# Phase 2: Analysis
jupyter nbconvert --to notebook --execute 02_explore.ipynb
jupyter nbconvert --to notebook --execute 03_clean.ipynb
jupyter nbconvert --to notebook --execute 04_features.ipynb
jupyter nbconvert --to notebook --execute 05_clustering.ipynb
jupyter nbconvert --to notebook --execute 06_analysis.ipynb
```

### Verify Data Integrity
```bash
# Open MinIO Console
open http://localhost:9001

# Navigate to buckets:
# - med-sandbox: Raw external data
# - med-data: Processed ML data (v1_raw, v2_clean, v3_features, v4_models)
```

---

## Success Criteria

Your pipeline execution is successful when:

- [x] All 10 notebooks execute without errors
- [x] `mimic_patient_selection.ipynb` shows "✅ VALIDATION PASSED"
- [x] `02_explore.ipynb` displays **3 source systems** (RxOut, BCMA, MIMIC-Community)
- [x] 10 patients show concurrent care in validation
- [x] `06_analysis.ipynb` identifies concurrent DDI scenarios
- [x] MinIO has all v1_raw, v2_clean, v3_features, v4_models outputs

---

## Next Steps After Pipeline Completion

1. **Review Concurrent DDI Analysis**: Focus on `06_analysis.ipynb` findings about cross-source DDIs
2. **Explore Care Coordination**: Identify medication reconciliation opportunities
3. **Refine Patient Mapping**: Update MIMIC subject IDs based on demographic similarity
4. **Expand Analysis**: Add custom analysis cells to explore specific DDI scenarios
5. **Document Insights**: Capture findings about "Blind Spot" DDI patterns

---

**Pipeline Version**: 2.0 (Option C: Concurrent Care)
**Last Updated**: 2025-12-02
**Status**: ✅ Ready for execution
