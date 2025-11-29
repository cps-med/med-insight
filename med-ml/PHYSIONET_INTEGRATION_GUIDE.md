# PhysioNet MIMIC-IV Integration Guide

**Phase 2: Community Care Medication Data Integration**

## Overview

This guide outlines the integration of PhysioNet MIMIC-IV clinical database into the Med-Insight med-ml subsystem to represent **community care (non-VA) treatment** of VA patients. This integration simulates real-world scenarios where veterans receive care at both VA facilities and community providers.

### Use Case

Expand the current 25-patient VA cohort to include community care medication episodes, enabling:
- **Care coordination analysis** across VA and non-VA providers
- **DDI detection** spanning multiple care settings
- **Transition of care** pattern identification
- **Medication reconciliation** challenges and opportunities

### Current State

- ✅ **Phase 1 Complete**: 25 VA patients with medications from RxOut (outpatient) and BCMA (inpatient)
- ✅ **Notebooks 01-06 Complete**: Data prep, exploration, cleaning, features, clustering, analysis
- 🔜 **Phase 2**: Add MIMIC-IV community care medications

### Data Source Strategy: MIMIC-IV Demo (Recommended)

**MIMIC-IV Clinical Database Demo** is the recommended data source for this integration:

✅ **Advantages:**
- **No credentialing required** - Openly accessible, start immediately
- **Sufficient data volume** - ~19,000 prescriptions, ~100 patients
- **Same schema** as full MIMIC-IV - All integration code works identically
- **Smaller dataset** - Faster downloads, easier to explore and process
- **Perfect for prototyping** - Can upgrade to full MIMIC-IV later if needed

📊 **Dataset Contents:**
- Prescriptions: ~19,000 medication orders
- Patients: ~100 unique patients
- Same tables: prescriptions, pharmacy, emar, emar_detail, patients, admissions

🎯 **For This Use Case:**
- Need: 10-15 patient medication profiles for community care integration
- Available: ~100 patients to choose from
- **Conclusion**: Demo dataset is more than sufficient

**Alternative: Full MIMIC-IV** (Optional)
- Requires PhysioNet credentialing (1-2 weeks)
- Contains 300K+ patients, 17M+ prescriptions
- Only needed if expanding beyond 25 patients significantly
- See "Optional: Full MIMIC-IV Access" section below for details

---

## Phase 2A: PhysioNet Setup & Exploration

### Step 1: Download MIMIC-IV Demo Dataset

**Timeline: Can start immediately (no approval needed)**

**Dataset Location:**
- Homepage: https://physionet.org/content/mimic-iv-demo/2.2/
- Files: https://physionet.org/content/mimic-iv-demo/2.2/hosp/#files-panel
- Version: 2.2 (or latest available)

**Download Instructions:**

```bash
# Create directory for MIMIC demo data
mkdir -p ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp
cd ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp

# Download required hosp module files (no authentication needed)
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/prescriptions.csv.gz
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/pharmacy.csv.gz
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/emar.csv.gz
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/emar_detail.csv.gz
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/patients.csv.gz
wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/admissions.csv.gz

# Unzip all files
gunzip *.gz

# Verify downloads
ls -lh
```

**Storage Requirements:**
- All hosp files compressed: ~50 MB
- Uncompressed: ~200 MB
- **Much smaller than full MIMIC-IV** (60+ GB)

**Files Overview:**

| File | Records | Description |
|------|---------|-------------|
| `prescriptions.csv` | ~19,000 | Medication orders (analogous to RxOut) |
| `pharmacy.csv` | ~13,000 | Pharmacy dispensing records |
| `emar.csv` | ~440,000 | Medication administrations (analogous to BCMA) |
| `emar_detail.csv` | ~3.8M | Detailed administration records |
| `patients.csv` | ~100 | Patient demographics |
| `admissions.csv` | ~500 | Hospital admissions |

### Step 2: Initial Data Exploration

**Quick exploration using Python:**

```python
import pandas as pd
import os

# Set data path
data_path = os.path.expanduser('~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp')

# Load key tables
df_prescriptions = pd.read_csv(f'{data_path}/prescriptions.csv')
df_patients = pd.read_csv(f'{data_path}/patients.csv')
df_admissions = pd.read_csv(f'{data_path}/admissions.csv')
df_emar = pd.read_csv(f'{data_path}/emar.csv')

print("=" * 60)
print("MIMIC-IV DEMO DATASET OVERVIEW")
print("=" * 60)
print(f"Prescriptions: {len(df_prescriptions):,} records")
print(f"Unique patients in prescriptions: {df_prescriptions['subject_id'].nunique()}")
print(f"Total patients: {len(df_patients)}")
print(f"Hospital admissions: {len(df_admissions):,}")
print(f"eMAR records: {len(df_emar):,}")
print(f"\nDate range (prescriptions): {df_prescriptions['starttime'].min()} to {df_prescriptions['starttime'].max()}")

# Sample patient medication profile
sample_subject = df_prescriptions['subject_id'].value_counts().index[0]
sample_meds = df_prescriptions[df_prescriptions['subject_id'] == sample_subject]
print(f"\nSample patient {sample_subject} medications:")
print(sample_meds[['drug', 'starttime', 'stoptime', 'route']].head(10))
```

**Expected Output:**
```
============================================================
MIMIC-IV DEMO DATASET OVERVIEW
============================================================
Prescriptions: 19,XXX records
Unique patients in prescriptions: ~85
Total patients: 100
Hospital admissions: ~500
eMAR records: 440,XXX

Date range (prescriptions): 2110-XX-XX to 2211-XX-XX
```

**Note**: MIMIC-IV uses shifted dates (year 2100-2200 range) to protect patient privacy. These will be remapped to 2024 dates during integration

### Step 3: Explore MIMIC-IV Medication Schema

**Key Tables:**

#### prescriptions
Medication orders written by providers (analogous to RxOut)

```sql
subject_id       -- Patient identifier (maps to PatientSID)
hadm_id          -- Hospital admission ID
pharmacy_id      -- Links to pharmacy table
starttime        -- Prescription start (maps to IssueDateTime)
stoptime         -- Prescription end (maps to ExpirationDateTime)
drug             -- Medication name (maps to DrugNameWithDose)
dose_val_rx      -- Dosage value
dose_unit_rx     -- Dosage unit
route            -- Administration route
frequency        -- Dosing frequency
```

#### emar (Electronic Medication Administration Record)
Actual medication administrations (analogous to BCMA)

```sql
subject_id       -- Patient identifier
hadm_id          -- Hospital admission ID
emar_id          -- eMAR record ID
charttime        -- Administration time (maps to ActionDateTime)
medication       -- Medication name
event_txt        -- Administration status (Given, Stopped, etc.)
dose_given       -- Actual dose administered
route            -- Administration route
```

#### pharmacy
Pharmacy dispensing records

```sql
subject_id       -- Patient identifier
hadm_id          -- Hospital admission ID
pharmacy_id      -- Unique pharmacy record ID
medication       -- Medication name
doses_per_24_hrs -- Dosing frequency
route            -- Administration route
```

**Exploration Queries:**

```sql
-- Count prescriptions by medication
SELECT drug, COUNT(*) as rx_count
FROM prescriptions
GROUP BY drug
ORDER BY rx_count DESC
LIMIT 20;

-- Sample patient medication profile
SELECT subject_id, drug, starttime, stoptime, route
FROM prescriptions
WHERE subject_id = 10000032
ORDER BY starttime;

-- eMAR administration patterns
SELECT medication, event_txt, COUNT(*) as event_count
FROM emar
GROUP BY medication, event_txt
ORDER BY event_count DESC
LIMIT 20;
```

**Comparison to VA Schema:**

| Aspect | MIMIC-IV | VA CDWWork |
|--------|----------|------------|
| Patient ID | `subject_id` (numeric) | `PatientSID` (numeric) + `PatientIEN` |
| Medication Orders | `prescriptions` table | `RxOut.RxOutpat` |
| Administrations | `emar` table | `BCMA.BCMAMedicationLog` |
| Drug Names | Free text, varied | Standardized VA formulary |
| Identifiers | No NDC codes | `LocalDrugSID`, `NationalDrugSID` |
| Date Format | Timestamps | Datetime + separate error fields |

### Optional: Full MIMIC-IV Access

**When to consider full MIMIC-IV:**

The Demo dataset is sufficient for most use cases, but consider full MIMIC-IV if:
- Expanding significantly beyond 25 VA patients (50-100+ patients)
- Need more diverse medication profiles than Demo provides
- Research requires larger sample sizes for statistical power
- Exploring less common medication combinations or conditions
- Demo dataset proves insufficient after initial integration

**How to obtain full MIMIC-IV access:**

1. **Create PhysioNet Account**
   - Visit: https://physionet.org/
   - Register (institutional email recommended)

2. **Complete CITI Training**
   - Course: "Data or Specimens Only Research"
   - URL: https://www.citiprogram.org/
   - Duration: ~2-3 hours
   - Save certificate PDF

3. **Request Access**
   - Navigate to: https://physionet.org/content/mimiciv/
   - Click "Request Access"
   - Upload CITI certificate
   - Sign Data Use Agreement
   - Provide research justification

4. **Wait for Approval**
   - Timeline: 1-2 weeks
   - Email notification when approved

5. **Download Full Dataset**
   - Use same download methods as Demo
   - Full hosp module: ~20 GB compressed
   - Contains 300K+ patients, 17M+ prescriptions

**Important Notes:**
- All integration code works identically with Demo and full MIMIC-IV
- Same schema, just larger volume
- Can upgrade from Demo to full MIMIC-IV anytime
- No changes needed to SQL scripts or notebooks

**Recommendation:** Start with Demo, upgrade only if needed.

---

## Phase 2B: Integration Design

### Step 4: Community Care Integration Strategy

**Recommended Approach: Dual-Source Episodes**

Represent veterans who transition between VA care and community care (MIMIC).

**Design Rationale:**
- Keeps existing 25 VA patients intact
- Adds community care "episodes" for subset of patients
- Simulates realistic care coordination scenarios
- Maintains clear source attribution

**Alternative Approaches:**

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Dual-Source Episodes** | Add community episodes for some patients | Realistic, clear attribution | More complex temporal logic |
| **Mixed Provider** | Intermix MIMIC meds with VA meds | Simulates concurrent care | Harder to distinguish sources |
| **Separate Cohort** | Add new patients from MIMIC only | Simplest implementation | Loses care coordination angle |

### Step 5: Key Design Decisions

#### Decision 1: Which Patients Get Community Care?

**Recommendation: 10-15 of the 25 patients**

**Selection Criteria:**
- Focus on complex patients (elderly, polypharmacy, multiple conditions)
- Prioritize patients with existing DDI scenarios
- Include mix of demographics and geographic locations

**Suggested Patient Subset:**

| PatientSID | Age | Conditions | VA Meds | Rationale |
|------------|-----|------------|---------|-----------|
| 1011 | 72 | AFib, CHF, HTN | 8 | Elderly, cardiac, high DDI risk |
| 1012 | 68 | Warfarin, NSAID, Aspirin | 7 | Bleeding risk, anticoagulation |
| 1013 | 77 | Multiple cardiac | 9 | Highest med count, complex |
| 1014 | 70 | NSAID, Warfarin | 8 | DDI scenario |
| 1015 | 82 | ACE-I, K-sparing, NSAID | 10 | Triple DDI, oldest patient |
| 1016 | 28 | PTSD, Depression | 3 | Mental health, younger |
| 1019 | 48 | Depression, HTN, SSRI+NSAID | 5 | Bleeding risk |
| 1021 | 58 | Diabetes, CHF | 6 | Chronic disease management |
| 1023 | 67 | Depression, Diabetes, Clopidogrel+PPI | 7 | DDI scenario |
| 1024 | 74 | CHF, AFib, CKD | 8 | Complex cardiac |

**Total: 10 patients** spanning ages 28-82, with community care episodes

#### Decision 2: Temporal Relationship Pattern

**Option A: Community → VA Transition** (Recommended)
- Community care occurs BEFORE current VA medications
- Simulates veteran entering VA system
- Timeline: Community care in 2024, VA care in 2025
- Use case: Medication reconciliation when patient transfers to VA

**Option B: VA → Community Transition**
- VA care occurs BEFORE community medications
- Simulates veteran leaving VA for community care
- Timeline: VA care early 2025, community care late 2025
- Use case: Care coordination when VA refers to community

**Option C: Concurrent Care**
- VA and community medications overlap in time
- Simulates dual-system utilization
- Timeline: Both sources active in 2025
- Use case: Veteran using both VA and private insurance

**Recommendation: Option A (Community → VA)**
- Most realistic for new VA enrollees
- Clear temporal separation simplifies analysis
- Enables "before/after" medication comparison

#### Decision 3: Community Care Data Volume

**Per-Patient Community Medications:**
- **Minimum**: 3-5 medications
- **Typical**: 5-8 medications
- **Complex**: 8-12 medications

**Recommendation: Match VA complexity**
- If patient has 8 VA meds, give 6-8 community meds
- Maintain polypharmacy patterns
- Include some medication continuity (e.g., chronic meds present in both sources)

**Timeline:**
- **Duration**: 60-90 days of community care
- **Date Range**: 2024-Q4 (October-December 2024)
- **VA Care Start**: 2025-Q1 (January 2025+)

#### Decision 4: Medication Selection Strategy

**Approach 1: Sample Real MIMIC Medications** (Most Realistic)
- Extract actual medication profiles from MIMIC-IV
- Select patients with similar demographics/conditions
- Preserve realistic medication combinations
- May require extensive data exploration

**Approach 2: Curated MIMIC-Style Medications** (Recommended)
- Manually create medication lists using MIMIC naming conventions
- Ensure DDI scenarios across VA/community boundary
- Full control over clinical scenarios
- Faster implementation

**Key Principles:**
1. **Medication Continuity**: Some meds continue from community → VA
2. **Medication Changes**: Some meds discontinued, new ones started
3. **Cross-Source DDIs**: Create scenarios where community med interacts with VA med
4. **Name Variation**: Use different drug names for same medication (e.g., "Warfarin" vs "Warfarin Sodium")

### Step 6: Schema Mapping Design

**Unified Medication Schema (CDWWork + MIMIC)**

Map MIMIC fields to existing CDWWork schema:

| MIMIC-IV Field | CDWWork Field | Mapping Notes |
|----------------|---------------|---------------|
| `subject_id` | `PatientSID` | Use lookup table: MIMIC ID → VA PatientSID |
| `hadm_id` | `InpatientSID` | Community admission ID (new series: 2000000+) |
| `drug` / `medication` | `DrugNameWithDose` | May need cleanup/normalization |
| `starttime` / `charttime` | `IssueDateTime` / `ActionDateTime` | Direct mapping |
| `stoptime` | `ExpirationDateTime` | Direct mapping |
| `route` | `Route` | Standardize values (PO, IV, etc.) |
| `dose_val_rx` + `dose_unit_rx` | `DosageOrdered` | Combine value + unit |
| `dose_given` | `DosageGiven` | For eMAR records |
| `frequency` | `Schedule` | Map to VA schedule codes |
| `event_txt` | `ActionStatus` / `ActionType` | Map "Given" → "GIVEN", etc. |

**New Field: SourceSystem**
- Existing: `'RxOut'`, `'BCMA'`
- New: `'MIMIC-Prescription'`, `'MIMIC-eMAR'`
- Or simplified: `'MIMIC-Community'`

**Patient Mapping Table:**

Create new table: `Dim.MIMICPatientMapping`

```sql
CREATE TABLE Dim.MIMICPatientMapping (
    MappingID INT PRIMARY KEY,
    VAPatientSID INT NOT NULL,           -- Links to SPatient.SPatient
    MIMICSubjectID INT NOT NULL,         -- Original MIMIC subject_id
    MappingRationale VARCHAR(500),       -- Why this pairing (age, gender, conditions)
    DateMapped DATE,
    FOREIGN KEY (VAPatientSID) REFERENCES SPatient.SPatient(PatientSID)
);
```

**Example Mappings:**

| VAPatientSID | MIMICSubjectID | Rationale |
|--------------|----------------|-----------|
| 1011 | 10000032 | 72yo male, CHF, AFib |
| 1012 | 10000084 | 68yo female, anticoagulation |
| 1013 | 10000175 | 77yo male, complex cardiac |

---

## Phase 2C: Implementation

### Architectural Approach: MinIO Medallion Pattern

**Recommended Strategy:** Follow the established medallion architecture pattern used for DDI reference data.

**Rationale:**
- ✅ **Consistent with existing architecture** - DDI and MIMIC are both external reference datasets
- ✅ **Separation of concerns** - CDWWork for VA operational data, MinIO for research datasets
- ✅ **Platform-independent** - Parquet files work everywhere (cloud-ready)
- ✅ **Integrates seamlessly** - Same notebook pattern as 01a, 01b, 01c
- ✅ **Simpler infrastructure** - No additional database needed

**Data Flow:**

```
Source:     med-sandbox/mimic-data/*.csv          (Raw MIMIC CSVs)
            ↓
Dataprep:   01d_dataprep_mimic.ipynb              (Convert to Parquet)
            ↓
Storage:    med-data/v1_raw/mimic/*.parquet       (Processed MIMIC)
            ↓
Analysis:   mimic_patient_selection.ipynb         (Select & transform)
            ↓
Integration: med-data/v1_raw/medications/*.parquet (Community care meds)
```

This mirrors the DDI pattern:
```
Source:     med-sandbox/kaggle-data/ddi/*.csv
Dataprep:   01a_dataprep_ddi.ipynb
Storage:    med-data/v1_raw/ddi/*.parquet
```

### Step 7: Upload MIMIC CSV Files to MinIO

**Upload to med-sandbox bucket:**

**Option A: Using MinIO Console (GUI)** - Simplest

1. Open MinIO Console: http://localhost:9001
2. Login with credentials from `.env`
3. Navigate to bucket: `med-sandbox`
4. Create folder: `mimic-data`
5. Upload all CSV files from `~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp/`
   - prescriptions.csv
   - pharmacy.csv
   - emar.csv
   - emar_detail.csv
   - patients.csv
   - admissions.csv

**Option B: Using MinIO Client (mc)** - Command-line

```bash
# Install MinIO client (if not already installed)
brew install minio/stable/mc

# Configure MinIO alias
mc alias set myminio http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Create mimic-data folder and upload files
cd ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp
mc cp prescriptions.csv myminio/med-sandbox/mimic-data/
mc cp pharmacy.csv myminio/med-sandbox/mimic-data/
mc cp emar.csv myminio/med-sandbox/mimic-data/
mc cp emar_detail.csv myminio/med-sandbox/mimic-data/
mc cp patients.csv myminio/med-sandbox/mimic-data/
mc cp admissions.csv myminio/med-sandbox/mimic-data/

# Verify upload
mc ls myminio/med-sandbox/mimic-data/
```

**Option C: Using Python/boto3** - Programmatic

```python
import boto3
import os
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

s3_client = boto3.client(
    's3',
    endpoint_url=f'http://{MINIO_ENDPOINT}',
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

# Upload files
data_path = os.path.expanduser('~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp')
files = ['prescriptions.csv', 'pharmacy.csv', 'emar.csv', 'emar_detail.csv', 'patients.csv', 'admissions.csv']

for file in files:
    file_path = f'{data_path}/{file}'
    s3_client.upload_file(file_path, 'med-sandbox', f'mimic-data/{file}')
    print(f'✓ Uploaded {file}')
```

**Verify MinIO Structure:**

```
MinIO med-sandbox bucket:
├── kaggle-data/
│   └── ddi/
│       └── db_drug_interactions.csv
└── mimic-data/                    # NEW
    ├── prescriptions.csv
    ├── pharmacy.csv
    ├── emar.csv
    ├── emar_detail.csv
    ├── patients.csv
    └── admissions.csv
```

### Step 8: Create New Dataprep Notebook for MIMIC

**Create:** `med-ml/src/01d_dataprep_mimic.ipynb`

This notebook converts MIMIC CSV files to Parquet format, following the same pattern as `01a_dataprep_ddi.ipynb`.

**Notebook Structure:**

```python
# Cell 1: Imports and Configuration
import pandas as pd
import logging
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

logger.info("MIMIC-IV Data Preparation - CSV to Parquet Conversion")
logger.info(f"Source: {SOURCE_BUCKET}/mimic-data/")
logger.info(f"Destination: {DEST_BUCKET}/v1_raw/mimic/")
```

```python
# Cell 2: Load MIMIC CSV Files from MinIO
from s3fs import S3FileSystem

# Initialize S3 filesystem
s3 = S3FileSystem(
    key=MINIO_ACCESS_KEY,
    secret=MINIO_SECRET_KEY,
    client_kwargs={'endpoint_url': f'http://{MINIO_ENDPOINT}'}
)

# Define source paths in med-sandbox
mimic_files = {
    'prescriptions': f's3://{SOURCE_BUCKET}/mimic-data/prescriptions.csv',
    'pharmacy': f's3://{SOURCE_BUCKET}/mimic-data/pharmacy.csv',
    'emar': f's3://{SOURCE_BUCKET}/mimic-data/emar.csv',
    'emar_detail': f's3://{SOURCE_BUCKET}/mimic-data/emar_detail.csv',
    'patients': f's3://{SOURCE_BUCKET}/mimic-data/patients.csv',
    'admissions': f's3://{SOURCE_BUCKET}/mimic-data/admissions.csv'
}

# Load each file
mimic_data = {}
for name, path in mimic_files.items():
    logger.info(f"Loading {name} from MinIO...")
    with s3.open(path, 'r') as f:
        mimic_data[name] = pd.read_csv(f)
    logger.info(f"  ✓ Loaded {len(mimic_data[name]):,} records")
```

```python
# Cell 3: Data Quality Check
logger.info("\nMIMIC-IV Demo Dataset Summary:")
logger.info("=" * 60)
logger.info(f"Prescriptions: {len(mimic_data['prescriptions']):,} records")
logger.info(f"Pharmacy: {len(mimic_data['pharmacy']):,} records")
logger.info(f"eMAR: {len(mimic_data['emar']):,} records")
logger.info(f"eMAR Detail: {len(mimic_data['emar_detail']):,} records")
logger.info(f"Patients: {len(mimic_data['patients']):,} records")
logger.info(f"Admissions: {len(mimic_data['admissions']):,} records")

# Check unique patients
logger.info(f"\nUnique patients with prescriptions: {mimic_data['prescriptions']['subject_id'].nunique()}")
logger.info(f"Date range: {mimic_data['prescriptions']['starttime'].min()} to {mimic_data['prescriptions']['starttime'].max()}")
```

```python
# Cell 4: Write to Parquet in med-data/v1_raw/mimic/
logger.info("\nWriting MIMIC data to Parquet format...")

for name, df in mimic_data.items():
    dest_path = f's3://{DEST_BUCKET}/v1_raw/mimic/{name}.parquet'
    logger.info(f"Writing {name} to {dest_path}...")

    with s3.open(dest_path, 'wb') as f:
        df.to_parquet(f, engine='pyarrow', index=False)

    logger.info(f"  ✓ Written {len(df):,} records")

logger.info("\n✅ MIMIC data preparation complete!")
logger.info(f"Data written to: {DEST_BUCKET}/v1_raw/mimic/")
```

**Add to config.py:**

```python
# MIMIC source and destination paths
SOURCE_MIMIC_PATH = "mimic-data/"
V1_RAW_MIMIC_PREFIX = "v1_raw/mimic/"
```

**MinIO Structure After Dataprep:**

```
med-data bucket:
├── v1_raw/
│   ├── ddi/
│   │   └── db_drug_interactions.parquet
│   ├── medications/
│   │   └── patient_medications.parquet
│   ├── demographics/
│   │   └── patient_demographics.parquet
│   └── mimic/                                  # NEW
│       ├── prescriptions.parquet
│       ├── pharmacy.parquet
│       ├── emar.parquet
│       ├── emar_detail.parquet
│       ├── patients.parquet
│       └── admissions.parquet
```

### Step 9: Create Patient Selection and Integration Notebook

**Create:** `med-ml/src/mimic_patient_selection.ipynb`

This notebook selects MIMIC patients matching VA patient profiles and transforms their medications to community care format.

**Notebook Structure:**

```python
# Cell 1: Imports and Setup
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from s3fs import S3FileSystem
from config import *

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

logger.info("MIMIC Patient Selection and Community Care Integration")
```

```python
# Cell 2: Load MIMIC Data from MinIO
s3 = S3FileSystem(
    key=MINIO_ACCESS_KEY,
    secret=MINIO_SECRET_KEY,
    client_kwargs={'endpoint_url': f'http://{MINIO_ENDPOINT}'}
)

# Load MIMIC Parquet files
logger.info("Loading MIMIC data from v1_raw/mimic/...")
with s3.open(f's3://{DEST_BUCKET}/v1_raw/mimic/prescriptions.parquet', 'rb') as f:
    df_mimic_rx = pd.read_parquet(f)

with s3.open(f's3://{DEST_BUCKET}/v1_raw/mimic/patients.parquet', 'rb') as f:
    df_mimic_patients = pd.read_parquet(f)

logger.info(f"Loaded {len(df_mimic_rx):,} prescriptions for {df_mimic_patients['subject_id'].nunique()} patients")
```

```python
# Cell 3: Define VA Patient Mapping
# Map 10 VA patients to MIMIC patients based on similar demographics

patient_mapping = pd.DataFrame([
    {'VAPatientSID': 1011, 'MIMICSubjectID': 10000032, 'Rationale': '72yo male, CHF, AFib, complex cardiac'},
    {'VAPatientSID': 1012, 'MIMICSubjectID': 10000084, 'Rationale': '68yo female, anticoagulation therapy'},
    {'VAPatientSID': 1013, 'MIMICSubjectID': 10000175, 'Rationale': '77yo male, polypharmacy, multiple cardiac meds'},
    {'VAPatientSID': 1014, 'MIMICSubjectID': 10000456, 'Rationale': '70yo female, NSAID + anticoagulation'},
    {'VAPatientSID': 1015, 'MIMICSubjectID': 10000623, 'Rationale': '82yo male, highest med count, renal concerns'},
    {'VAPatientSID': 1016, 'MIMICSubjectID': 10000891, 'Rationale': '28yo male, mental health, PTSD'},
    {'VAPatientSID': 1019, 'MIMICSubjectID': 10001204, 'Rationale': '48yo female, depression + HTN'},
    {'VAPatientSID': 1021, 'MIMICSubjectID': 10001587, 'Rationale': '58yo female, diabetes, CHF'},
    {'VAPatientSID': 1023, 'MIMICSubjectID': 10001923, 'Rationale': '67yo female, depression, diabetes'},
    {'VAPatientSID': 1024, 'MIMICSubjectID': 10002341, 'Rationale': '74yo male, complex cardiac, CKD'}
])

logger.info(f"Defined mapping for {len(patient_mapping)} VA patients to MIMIC patients")
```

```python
# Cell 4: Extract and Transform MIMIC Medications
# Select medications for mapped patients
mimic_subjects = patient_mapping['MIMICSubjectID'].tolist()
df_selected = df_mimic_rx[df_mimic_rx['subject_id'].isin(mimic_subjects)].copy()

logger.info(f"Selected {len(df_selected):,} prescriptions for mapped patients")

# Transform MIMIC dates from 2100s to 2024 (Community → VA transition)
# MIMIC uses 2100-2200 range; shift to Oct-Dec 2024
def shift_date_to_2024(date_str):
    """Shift MIMIC dates (2100s) to 2024 Q4"""
    if pd.isna(date_str):
        return None
    dt = pd.to_datetime(date_str)
    # Shift year to 2024 and month to Q4
    return dt.replace(year=2024, month=10 + (dt.month % 3))

df_selected['starttime_2024'] = df_selected['starttime'].apply(shift_date_to_2024)
df_selected['stoptime_2024'] = df_selected['stoptime'].apply(shift_date_to_2024)

# Map MIMIC subject_id to VA PatientSID
df_selected = df_selected.merge(
    patient_mapping[['VAPatientSID', 'MIMICSubjectID']],
    left_on='subject_id',
    right_on='MIMICSubjectID',
    how='left'
)
```

```python
# Cell 5: Create Community Care Medication Records
# Transform to match VA medication schema

df_community_care = pd.DataFrame({
    'PatientSID': df_selected['VAPatientSID'],
    'Sta3n': 999,  # Community care indicator
    'DrugNameWithoutDose': df_selected['drug'].str.extract(r'([A-Za-z\s]+)')[0].str.strip(),
    'DrugNameWithDose': df_selected['drug'],
    'SourceSystem': 'MIMIC-Community',
    'MedicationDateTime': df_selected['starttime_2024'],
    'StartDate': df_selected['starttime_2024'],
    'EndDate': df_selected['stoptime_2024'],
    'Status': 'ACTIVE',
    'Route': df_selected['route'],
    'DosageOrdered': df_selected['dose_val_rx'].astype(str) + ' ' + df_selected['dose_unit_rx'].astype(str),
    'Frequency': df_selected['frequency'],
    'PrescriptionNumber': 'CC-' + df_selected['pharmacy_id'].astype(str),
    'PharmacyName': 'Community Pharmacy',
    'ProviderType': 'Community Provider'
})

logger.info(f"Created {len(df_community_care):,} community care medication records")
logger.info(f"Date range: {df_community_care['StartDate'].min()} to {df_community_care['StartDate'].max()}")
```

```python
# Cell 6: Load Existing VA Medications
logger.info("Loading existing VA medications...")
with s3.open(f's3://{DEST_BUCKET}/v1_raw/medications/patient_medications.parquet', 'rb') as f:
    df_va_meds = pd.read_parquet(f)

logger.info(f"Loaded {len(df_va_meds):,} VA medication records")
```

```python
# Cell 7: Merge and Write Combined Dataset
# Combine VA and community care medications
df_combined = pd.concat([df_va_meds, df_community_care], ignore_index=True)
df_combined = df_combined.sort_values(['PatientSID', 'MedicationDateTime'])

logger.info(f"\nCombined Dataset Summary:")
logger.info(f"Total records: {len(df_combined):,}")
logger.info(f"Total patients: {df_combined['PatientSID'].nunique()}")
logger.info(f"\nSource Distribution:")
logger.info(df_combined['SourceSystem'].value_counts())

# Write to v1_raw/medications/ (replacing existing)
dest_path = f's3://{DEST_BUCKET}/v1_raw/medications/patient_medications.parquet'
logger.info(f"\nWriting combined dataset to {dest_path}...")

with s3.open(dest_path, 'wb') as f:
    df_combined.to_parquet(f, engine='pyarrow', index=False)

logger.info("✅ Community care integration complete!")
```

```python
# Cell 8: Validation
# Verify integration quality
logger.info("\n" + "=" * 60)
logger.info("VALIDATION CHECKS")
logger.info("=" * 60)

# Check 1: Patient count with community care
community_patients = df_combined[df_combined['SourceSystem'] == 'MIMIC-Community']['PatientSID'].unique()
logger.info(f"✓ Patients with community care: {len(community_patients)}")
logger.info(f"  Expected: 10, Got: {len(community_patients)}")

# Check 2: Temporal separation (community before VA)
for patient in community_patients:
    patient_meds = df_combined[df_combined['PatientSID'] == patient]
    community_start = patient_meds[patient_meds['SourceSystem'] == 'MIMIC-Community']['StartDate'].min()
    va_start = patient_meds[patient_meds['SourceSystem'].isin(['RxOut', 'BCMA'])]['StartDate'].min()

    if pd.notna(community_start) and pd.notna(va_start):
        if community_start >= va_start:
            logger.warning(f"  ⚠ Patient {patient}: Community care NOT before VA care")
        else:
            logger.info(f"  ✓ Patient {patient}: Community ({community_start.date()}) → VA ({va_start.date()})")

logger.info("\n✅ Integration validation complete!")
```

**Notes:**
- MIMIC dates are shifted from 2100-2200 range to Oct-Dec 2024 (Q4 2024)
- VA care starts in 2025 (Q1 2025), creating clear temporal separation
- `Sta3n = 999` marks community care records
- Patient mapping can be refined based on actual MIMIC patient demographics

### Step 10: Existing Notebooks Work Automatically

**No changes needed to existing notebooks!**

The beauty of the MinIO medallion approach is that `mimic_patient_selection.ipynb` (Step 9) replaces the `v1_raw/medications/patient_medications.parquet` file with the combined dataset. All downstream notebooks automatically work with the new data.

**Workflow:**

```
1. Run 01a_dataprep_ddi.ipynb          (DDI data - unchanged)
2. Run 01b_dataprep_medications.ipynb  (VA meds only - unchanged)
3. Run 01c_dataprep_demographics.ipynb (Demographics - unchanged)
4. Run 01d_dataprep_mimic.ipynb        (NEW - MIMIC CSV → Parquet)
5. Run mimic_patient_selection.ipynb   (NEW - Integrate community care)
   ↳ Replaces v1_raw/medications/patient_medications.parquet with combined VA + Community dataset
6. Run 02_explore.ipynb                (Automatically sees 3 sources: RxOut, BCMA, MIMIC-Community)
7. Run 03_clean.ipynb                  (Works with combined data)
8. Run 04_features.ipynb               (Enhanced features with community care)
9. Run 05_clustering.ipynb             (Better clustering with dual-source data)
10. Run 06_analysis.ipynb              (Care coordination insights)
```

**Optional: Enhanced Analysis in 02_explore.ipynb**

You may want to add a cell to verify community care integration:

```python
# Add this cell to 02_explore.ipynb after loading medications

# Community Care Integration Check
logger.info("\n" + "=" * 60)
logger.info("COMMUNITY CARE INTEGRATION ANALYSIS")
logger.info("=" * 60)

# Source distribution
logger.info("\nSource System Distribution:")
source_counts = df_medications['SourceSystem'].value_counts()
print(source_counts)

# Community care patients
if 'MIMIC-Community' in df_medications['SourceSystem'].values:
    community_patients = df_medications[df_medications['SourceSystem'] == 'MIMIC-Community']['PatientSID'].unique()
    logger.info(f"\nPatients with community care: {len(community_patients)}")
    logger.info(f"Community care patients: {sorted(community_patients)}")

    # Temporal analysis
    for patient in community_patients[:3]:  # Show first 3 as examples
        patient_meds = df_medications[df_medications['PatientSID'] == patient]
        community = patient_meds[patient_meds['SourceSystem'] == 'MIMIC-Community']
        va = patient_meds[patient_meds['SourceSystem'].isin(['RxOut', 'BCMA'])]

        logger.info(f"\nPatient {patient}:")
        logger.info(f"  Community meds: {len(community)} ({community['StartDate'].min().date()} to {community['StartDate'].max().date()})")
        logger.info(f"  VA meds: {len(va)} ({va['MedicationDateTime'].min().date() if len(va) > 0 else 'N/A'} onward)")
else:
    logger.info("\n⚠ No community care data found. Run mimic_patient_selection.ipynb first.")
```

**Optional: Update config.py**

Add MIMIC configuration constants:

```python
# MIMIC source and destination paths
SOURCE_MIMIC_PATH = "mimic-data/"
V1_RAW_MIMIC_PREFIX = "v1_raw/mimic/"

# Community care indicator
COMMUNITY_CARE_STA3N = 999

# Date range to include community care (if not already covering 2024)
DEFAULT_START_DATE = date(2024, 1, 1)  # Extends to include Q4 2024 community care
DEFAULT_END_DATE = date(2025, 12, 31)
```

---

## Phase 2D: Validation & Analysis

### Step 11: Validate Integration

**Validation is built into `mimic_patient_selection.ipynb` (Step 9, Cell 8), but you can also validate in notebooks:**

**Create validation notebook or add cells to 02_explore.ipynb:**

```python
# Load combined medication dataset
from s3fs import S3FileSystem
from config import *

s3 = S3FileSystem(
    key=MINIO_ACCESS_KEY,
    secret=MINIO_SECRET_KEY,
    client_kwargs={'endpoint_url': f'http://{MINIO_ENDPOINT}'}
)

with s3.open(f's3://{DEST_BUCKET}/v1_raw/medications/patient_medications.parquet', 'rb') as f:
    df_medications = pd.read_parquet(f)

logger.info("=" * 60)
logger.info("COMMUNITY CARE INTEGRATION VALIDATION")
logger.info("=" * 60)
```

**Validation Checks:**

1. **Patient Count**
   ```python
   # Should have 10 patients with community care
   community_patients = df_medications[
       df_medications['SourceSystem'] == 'MIMIC-Community'
   ]['PatientSID'].nunique()

   logger.info(f"\n1. Patient Count Check:")
   logger.info(f"   Patients with community care: {community_patients}")
   logger.info(f"   Expected: 10, Got: {community_patients}")
   assert community_patients == 10, "Expected 10 patients with community care"
   logger.info("   ✓ PASS")
   ```

2. **Medication Count**
   ```python
   # Should have community medications (varies by MIMIC selection)
   community_meds = len(df_medications[df_medications['SourceSystem'] == 'MIMIC-Community'])

   logger.info(f"\n2. Medication Count Check:")
   logger.info(f"   Community care medications: {community_meds}")
   logger.info(f"   Expected: 40-100, Got: {community_meds}")
   assert community_meds >= 40, "Expected at least 40 community medications"
   logger.info("   ✓ PASS")
   ```

3. **Date Range**
   ```python
   # Community care should be in 2024 Q4
   community_data = df_medications[df_medications['SourceSystem'] == 'MIMIC-Community']
   earliest = community_data['StartDate'].min()
   latest = community_data['StartDate'].max()

   logger.info(f"\n3. Date Range Check:")
   logger.info(f"   Earliest community care: {earliest}")
   logger.info(f"   Latest community care: {latest}")
   logger.info(f"   Expected: Oct-Dec 2024")
   assert earliest.year == 2024 and earliest.month >= 10, "Community care should start in Q4 2024"
   assert latest.year == 2024, "Community care should be in 2024"
   logger.info("   ✓ PASS")
   ```

4. **Temporal Separation**
   ```python
   # Verify community care comes before VA care
   logger.info(f"\n4. Temporal Separation Check:")

   community_patient_ids = [1011, 1012, 1013, 1014, 1015, 1016, 1019, 1021, 1023, 1024]
   temporal_issues = []

   for patient in community_patient_ids:
       patient_meds = df_medications[df_medications['PatientSID'] == patient]
       community = patient_meds[patient_meds['SourceSystem'] == 'MIMIC-Community']
       va = patient_meds[patient_meds['SourceSystem'].isin(['RxOut', 'BCMA'])]

       if len(community) > 0 and len(va) > 0:
           comm_start = community['StartDate'].min()
           va_start = va['MedicationDateTime'].min()

           if comm_start >= va_start:
               temporal_issues.append(patient)
               logger.warning(f"   ⚠ Patient {patient}: Community NOT before VA")
           else:
               logger.info(f"   ✓ Patient {patient}: Community ({comm_start.date()}) → VA ({va_start.date()})")

   if len(temporal_issues) == 0:
       logger.info("   ✓ PASS - All community care precedes VA care")
   else:
       logger.error(f"   ✗ FAIL - Temporal issues for patients: {temporal_issues}")
   ```

5. **Source System Distribution**
   ```python
   # Check all three sources present
   logger.info(f"\n5. Source System Distribution:")
   source_counts = df_medications['SourceSystem'].value_counts()
   print(source_counts)

   expected_sources = {'RxOut', 'BCMA', 'MIMIC-Community'}
   actual_sources = set(source_counts.index)

   if expected_sources.issubset(actual_sources):
       logger.info("   ✓ PASS - All 3 source systems present")
   else:
       missing = expected_sources - actual_sources
       logger.error(f"   ✗ FAIL - Missing sources: {missing}")
   ```

6. **Data Quality**
   ```python
   logger.info(f"\n6. Data Quality Checks:")

   # No null drug names
   null_drugs = df_medications['DrugNameWithDose'].isna().sum()
   logger.info(f"   Null drug names: {null_drugs} (Expected: 0)")
   assert null_drugs == 0, "Found null drug names"

   # All dates valid
   null_dates = df_medications['MedicationDateTime'].isna().sum()
   logger.info(f"   Null dates: {null_dates} (Expected: 0)")
   assert null_dates == 0, "Found null dates"

   # Check for duplicates
   duplicates = df_medications.duplicated().sum()
   logger.info(f"   Duplicate records: {duplicates} (Expected: 0)")

   # Proper source attribution
   valid_sources = df_medications['SourceSystem'].isin(['RxOut', 'BCMA', 'MIMIC-Community']).all()
   logger.info(f"   Valid source systems: {valid_sources}")
   assert valid_sources, "Found invalid source systems"

   logger.info("   ✓ PASS - Data quality checks passed")
   ```

7. **DDI Detection Across Sources** (Example)
   ```python
   # Check for DDIs spanning community and VA care
   logger.info(f"\n7. Cross-Source DDI Detection (Example):")

   # Example: Patient on Warfarin (community) + NSAID (VA)
   patient_1011_meds = df_medications[
       (df_medications['PatientSID'] == 1011) &
       (df_medications['DrugNameWithoutDose'].str.contains('WARFARIN|IBUPROFEN|NAPROXEN', case=False, na=False))
   ]

   if len(patient_1011_meds) > 0:
       logger.info(f"   Found {len(patient_1011_meds)} potential DDI medications for Patient 1011:")
       print(patient_1011_meds[['SourceSystem', 'DrugNameWithDose', 'MedicationDateTime']].sort_values('MedicationDateTime'))
   else:
       logger.info("   No example DDI found (depends on MIMIC patient selection)")
   ```

### Step 12: Re-run Complete Pipeline

**Execution Order:**

```bash
# Navigate to med-ml directory
cd ~/swdev/med/med-insight/med-ml/src

# Activate virtual environment
source ../../.venv/bin/activate

# Execute notebooks in order
jupyter nbconvert --to notebook --execute 01a_dataprep_ddi.ipynb
jupyter nbconvert --to notebook --execute 01b_dataprep_medications.ipynb
jupyter nbconvert --to notebook --execute 01c_dataprep_demographics.ipynb
jupyter nbconvert --to notebook --execute 01d_dataprep_mimic.ipynb          # NEW
jupyter nbconvert --to notebook --execute mimic_patient_selection.ipynb     # NEW
jupyter nbconvert --to notebook --execute 02_explore.ipynb
jupyter nbconvert --to notebook --execute 03_clean.ipynb
jupyter nbconvert --to notebook --execute 04_features.ipynb
jupyter nbconvert --to notebook --execute 05_clustering.ipynb
jupyter nbconvert --to notebook --execute 06_analysis.ipynb
```

**Alternative: Run in VS Code**

Open each notebook in VS Code and run all cells interactively.

**Expected Changes:**

| Notebook | Before (VA only) | After (VA + Community) | Change |
|----------|------------------|------------------------|--------|
| 01d | N/A | MIMIC CSV → Parquet | New: 6 MIMIC tables in v1_raw/mimic/ |
| mimic_patient_selection | N/A | Patient mapping & integration | New: Combined medications dataset |
| 01b | 25 patients, ~79 meds | Unchanged | VA medications baseline |
| 02 | 2 sources (RxOut, BCMA) | 3 sources (RxOut, BCMA, MIMIC-Community) | +1 source, +40-100 meds |
| 03 | VA cleaning rules | Same rules apply to all sources | Automatic |
| 04 | Features for VA only | Enhanced with community patterns | Temporal features richer |
| 05 | Clusters based on VA only | Dual-source clustering | Better stratification |
| 06 | VA-only analysis | Care coordination insights | New analysis dimension |

### Step 13: Analyze Community Care Impact

**New Analysis Questions:**

1. **Care Coordination:**
   - How many medications continue from community → VA?
   - How many are discontinued at transition?
   - How many new medications start at VA?

2. **DDI Detection:**
   - How many DDIs span community/VA boundary?
   - Do DDIs exist in community care that VA doesn't see?
   - Are community DDIs resolved or perpetuated in VA?

3. **Medication Reconciliation:**
   - Name variations for same drug (Warfarin vs Warfarin Sodium)
   - Dose changes at transition
   - Formulary substitutions

4. **Risk Stratification:**
   - Do patients with community care cluster differently?
   - Does community medication history predict VA complexity?
   - Transition risk factors

**Sample Analysis Code:**

```python
# In 06_analysis.ipynb

# Analyze care transitions for community care patients
community_patients = [1011, 1012, 1013, 1014, 1015, 1016, 1019, 1021, 1023, 1024]

for patient in community_patients:
    patient_meds = df_medications[df_medications['PatientSID'] == patient]

    community_meds = patient_meds[patient_meds['SourceSystem'] == 'MIMIC-Community']
    va_meds = patient_meds[patient_meds['SourceSystem'].isin(['RxOut', 'BCMA'])]

    # Find continuing medications (same drug in both)
    community_drugs = set(community_meds['DrugNameWithoutDose'])
    va_drugs = set(va_meds['DrugNameWithoutDose'])
    continuing = community_drugs.intersection(va_drugs)
    discontinued = community_drugs - va_drugs
    new_va = va_drugs - community_drugs

    print(f"Patient {patient}:")
    print(f"  Continuing: {len(continuing)} meds - {continuing}")
    print(f"  Discontinued: {len(discontinued)} meds - {discontinued}")
    print(f"  New at VA: {len(new_va)} meds - {new_va}")
    print()
```

---

## Next Actions

### Immediate - Day 1 (Today!)

1. ✅ **Review this guide** - Understand the full integration plan
2. ⏳ **Download MIMIC-IV Demo** - Execute Step 1 download commands
   ```bash
   mkdir -p ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp
   cd ~/swdev/med/med-insight/med-data/physionet/mimic-iv-demo/hosp
   wget https://physionet.org/files/mimic-iv-demo/2.2/hosp/prescriptions.csv.gz
   # ... (see Step 1 for all files)
   ```
3. ⏳ **Initial exploration** - Run Step 2 Python exploration code
4. ⏳ **Make design decisions**:
   - Confirm 10 patients for community care integration
   - Choose temporal pattern (recommend: Community → VA)
   - Decide on medication volume per patient (5-8 meds each)

### Week 1 - Patient Selection

5. ⏳ **Explore MIMIC Demo patients** - Analyze demographics, medication patterns
6. ⏳ **Select matching patients** - Find 10-15 MIMIC patients that match VA patient profiles
   - Similar age (±5-10 years)
   - Similar gender
   - Similar medication complexity
   - Similar conditions (cardiac, diabetes, mental health, etc.)
7. ⏳ **Create patient mapping** - Document MIMIC → VA patient mappings
8. ⏳ **Design medication scenarios**:
   - Plan medication continuity (some meds continue to VA)
   - Plan medication changes (some discontinued, some new)
   - Include DDI scenarios across community/VA boundary

### Week 2 - Implementation

9. ⏳ **Create patient mapping script** - `create_mimic_patient_mapping.sql`
10. ⏳ **Extract MIMIC medication data** - Get medications for selected patients
11. ⏳ **Build integration script** - Create `add_community_care_mimic.sql`
    - Transform MIMIC dates from 2100s → 2024
    - Map MIMIC drug names to CDWWork format
    - Set Sta3n = 999 for community care flag
12. ⏳ **Load and test** - Execute scripts, verify data in database

### Week 2-3 - Validation & Analysis

13. ⏳ **Update notebooks** - Modify `01b_dataprep_medications.ipynb` for 3 sources
14. ⏳ **Re-run pipeline** - Execute notebooks 01b through 06
15. ⏳ **Validate integration** - Check patient counts, medication counts, dates
16. ⏳ **Analyze results** - Care coordination patterns, cross-source DDIs
17. ✅ **Phase 2 Complete!** - Community care integration successful

### Timeline Summary

| Phase | Duration | Status |
|-------|----------|--------|
| Download & Explore | 1 day | ⏳ Ready to start |
| Patient Selection | 3-4 days | ⏳ Pending |
| Implementation | 4-5 days | ⏳ Pending |
| Validation & Analysis | 2-3 days | ⏳ Pending |
| **Total** | **~2 weeks** | vs 4-6 weeks with full MIMIC |

### Optional: Full MIMIC-IV Access (Future)

If you later need the full MIMIC-IV dataset (300K+ patients):

1. **Apply for PhysioNet access** - Start credentialing process
2. **Complete CITI training** - Data research ethics course (~2-3 hours)
3. **Request MIMIC-IV access** - Upload certificate, sign DUA
4. **Wait for approval** - Typical timeline: 1-2 weeks
5. **Download full dataset** - Same schema as Demo, larger volume
6. **Update scripts** - No changes needed, works identically

**When to consider full MIMIC-IV:**
- Expanding beyond 25 VA patients significantly (50+ patients)
- Need more diverse medication profiles
- Research requires larger sample size
- Demo dataset proves insufficient

**For current use case** (25 VA patients + 10 community care episodes): **Demo is sufficient!**

---

## Resources

### PhysioNet - MIMIC-IV Demo (Primary)

- **MIMIC-IV Demo Homepage**: https://physionet.org/content/mimic-iv-demo/2.2/
- **Demo Files (hosp module)**: https://physionet.org/content/mimic-iv-demo/2.2/hosp/#files-panel
- **MIMIC-IV Documentation**: https://mimic.mit.edu/docs/iv/
- **Demo Overview**: https://mimic.mit.edu/docs/iv/demo/

### PhysioNet - Full MIMIC-IV (Optional)

- **MIMIC-IV Full Homepage**: https://physionet.org/content/mimiciv/
- **CITI Training**: https://www.citiprogram.org/
- **PhysioNet Credentialing**: https://physionet.org/settings/credentialing/
- **Data Use Agreement**: https://physionet.org/content/mimiciv/view-dua/2.2/

### MIMIC-IV Schema Documentation

- **Tables Overview**: https://mimic.mit.edu/docs/iv/modules/hosp/
- **Prescriptions Table**: https://mimic.mit.edu/docs/iv/modules/hosp/prescriptions/
- **eMAR Table**: https://mimic.mit.edu/docs/iv/modules/hosp/emar/
- **Pharmacy Table**: https://mimic.mit.edu/docs/iv/modules/hosp/pharmacy/
- **Patients Table**: https://mimic.mit.edu/docs/iv/modules/hosp/patients/
- **Admissions Table**: https://mimic.mit.edu/docs/iv/modules/hosp/admissions/

### Med-Insight Guides

- **CLUSTERING_AND_ANALYSIS_GUIDE.md** - Phase 1 clustering methodology
- **FEATURE_ENGINEERING_GUIDE.md** - Patient-level feature design
- **DEMOGRAPHICS_IMPLEMENTATION.md** - Demographics integration approach
- **expansion_patient_design.md** - Phase 1 expansion patient profiles

### Related Files

- `med-data/sql-server/cdwwork/insert/_master.sql` - Base patient data
- `med-data/sql-server/cdwwork/insert/add_elderly_patients.sql` - Elderly cohort
- `med-data/sql-server/cdwwork/insert/add_expansion_patients.sql` - Phase 1 expansion
- `med-ml/src/01b_dataprep_medications.ipynb` - Medication data prep notebook
- `med-ml/src/config.py` - Centralized configuration

---

## Appendix: Alternative Approaches

### Alternative 1: Full MIMIC Patient Import

Instead of mapping MIMIC to existing VA patients, import MIMIC patients as new records.

**Pros:**
- Larger dataset (can add 50-100+ patients)
- Real MIMIC data, no curation needed
- Supports supervised learning with larger N

**Cons:**
- Loses care coordination use case
- No VA/community comparison
- Different data quality/completeness

### Alternative 2: Synthetic MIMIC-Style Data

Generate synthetic community care data without PhysioNet access.

**Pros:**
- No credentialing required
- Full control over scenarios
- Faster implementation

**Cons:**
- Not real-world data
- Lacks MIMIC's realism
- Limited validation

### Alternative 3: Other Community Data Sources

Consider alternatives to MIMIC-IV:

- **eICU Collaborative Research Database** - Multi-center ICU data
- **OMOP CDM Sample Datasets** - Standardized format
- **Synthea** - Synthetic patient generator
- **CMS Public Use Files** - Medicare claims data

---

## Document Version

- **Version**: 1.2
- **Created**: 2024-11-29
- **Last Updated**: 2024-11-29
- **Status**: Phase 2 Planning - Ready for Immediate Implementation
- **Major Changes**:
  - v1.0 - Initial guide with full MIMIC-IV credentialing approach
  - v1.1 - Updated to prioritize MIMIC-IV Demo (no credentialing required)
  - v1.2 - **Architectural shift to MinIO medallion pattern** (consistency with DDI approach)
- **Architecture**: MinIO medallion (med-sandbox → v1_raw → integration via Parquet)
- **Next Review**: After MIMIC-IV Demo integration complete

---

**Ready to proceed with PhysioNet MIMIC-IV Demo integration - Start today!**
