# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Med-Insight** is an AI-powered, full-stack healthcare analytics application for providers to deliver safer, higher-quality care by transforming complex patient treatment data into actionable insights. The platform integrates data from multiple clinical systems, performs ETL processing, and applies AI/ML techniques to uncover patterns and trends.

This is a **monorepo** with four independent subsystems, each with its own technology stack, dependencies, and setup requirements.

## Repository Structure

```
med-insight/                    # Monorepo root
├── med-data/                   # Mock data sources for development/testing
├── med-etl/                    # ETL pipeline for data preparation
├── med-ml/                     # AI and machine learning layer
├── med-view/                   # Web UI dashboard (FastAPI + HTMX)
├── .env                        # Shared environment variables (NOT in git)
├── .venv/                      # Root-level Python virtual environment
└── requirements.txt            # Root-level Python dependencies
```

**Important**: Each subsystem has its own README.md with detailed setup instructions. Always consult the subsystem-specific README when working within that directory.

## External Dependencies

### Output Directory Structure
The application requires an external output directory **outside** version control:

```bash
# Create external output directories (REQUIRED before first run)
cd <parent folder of med-insight>
mkdir -p med-output/extract
mkdir -p med-output/log
```

Expected directory layout:
```
.                          # Parent folder
├── med-insight/           # Application code (under git)
└── med-output/            # Output files (NOT under git)
    ├── extract/           # Clinical data extract files
    └── log/               # Application logs
```

### Shared Infrastructure (via med-data)
All subsystems rely on shared infrastructure managed by **med-data**:
- **Docker Desktop** or Podman for containers
- **SQL Server 2019** container (`sqlserver2019`)
- **CDWWork database** - Mock VA Clinical Data Warehouse
- **MinIO container** (`med-insight-minio`) - S3-compatible object storage
- **Python 3.11** via Homebrew
- **ODBC Driver 18 for SQL Server**

**Setup order**: Always set up **med-data** first, then proceed to other subsystems.

## Development Commands

### Starting Development Session

```bash
# 1. Start Docker Desktop (if not auto-starting)
# Launch from Applications or dock

# 2. Start containers
docker start sqlserver2019 med-insight-minio

# 3. Verify containers running
docker ps

# 4. Navigate to appropriate subsystem
cd ~/swdev/med/med-insight/<subsystem>

# 5. Activate Python virtual environment
source .venv/bin/activate
```

### med-view: Web Dashboard

```bash
# Navigate to med-view directory
cd ~/swdev/med/med-insight/med-view

# Activate environment
source .venv/bin/activate

# Start development server
uvicorn main:app --reload

# Access in browser
# http://127.0.0.1:8000/

# Stop server
# CTRL + C
```

**Tech Stack**: FastAPI + HTMX + Jinja2 + Server-Side Rendering

### med-etl: Data Pipeline

```bash
# Navigate to med-etl directory
cd ~/swdev/med/med-insight/med-etl

# Activate environment
source .venv/bin/activate

# Run interactive ETL application
python main.py
# Follow prompts for ETL function, station, extract type, date range, status
```

**Entry Point**: `main.py` provides interactive CLI for ETL operations
**Extract Types**: ADM (admissions), LBB (lab blood bank), RAD (radiology), CLI (clinic)

### med-ml: AI/ML Analysis

```bash
# Navigate to med-ml directory
cd ~/swdev/med/med-insight/med-ml/src

# Activate environment
source ../../.venv/bin/activate

# Start JupyterLab
jupyter lab
# Access at: http://localhost:8888

# OR use VS Code with Jupyter extension
# Open .ipynb files directly in VS Code
# Select kernel: .venv (Python 3.11)
```

**Tech Stack**: JupyterLab + Pandas + scikit-learn + MinIO + SQL Server
**Notebooks**:
- `01a/b/c_dataprep_*.ipynb` - Data preparation (DDI, medications, demographics) ✅
- `02_explore.ipynb` - Exploratory data analysis ✅
- `03_clean.ipynb` - Data cleaning ✅
- `04_features.ipynb` - Feature engineering ✅
- `05_clustering.ipynb` - Patient risk clustering 🔄
- `06_analysis.ipynb` - Results analysis 🔜

**Data Storage**: MinIO medallion architecture (v1_raw → v2_clean → v3_features → v4_models)

### med-data: Database and Mock Data

```bash
# Navigate to med-data directory
cd ~/swdev/med/med-insight/med-data

# Create CDWWork database (FIRST TIME ONLY)
cd sql-server/cdwwork/create
./_master.sh

# Populate with base sample data (FIRST TIME ONLY)
cd ../insert
./_master.sh

# Optional: Expand patient cohort
# Option 1: Add elderly patient cohort (15 total patients)
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -d CDWWork -i add_elderly_patients.sql
# Adds 5 elderly patients (ages 68-82) with 18 DDI scenarios

# Option 2: Add expansion cohort (25 total patients)
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -d CDWWork -i add_expansion_patients.sql
# Adds 10 patients with balanced age/complexity distribution, mental health emphasis

# Generate sample extract files
cd ~/swdev/med/med-insight/med-data
source .venv/bin/activate
python src/create_sample_extract.py
```

### Database Access

```bash
# Connect to SQL Server via sqlcmd
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD"

# Query CDWWork database (source data from med-data)
sqlcmd -S 127.0.0.1,1433 -U sa -P "$CDWWORK_DB_PASSWORD" -d CDWWork -Q "SELECT COUNT(*) FROM Inpat.Inpatient"

# Query Extract database (prepared data from med-etl)
sqlcmd -S 127.0.0.1,1433 -U sa -P "$EXTRACT_DB_PASSWORD" -d Extract -Q "SELECT COUNT(*) FROM Data.ADM"

# MinIO Console (object storage)
# http://localhost:9001
# Username: admin (from .env)
```

**VS Code Integration**: Use the mssql extension for SQL Server connectivity. Connection profile:
- Server: `127.0.0.1,1433` (note the comma, not colon)
- Auth: SQL Login, username `sa`
- Trust server certificate: yes

### Testing

No formal test suite is currently implemented. Testing is primarily manual via:
- Running ETL pipelines with sample data
- Verifying database records via SQL queries
- Accessing web dashboard and verifying UI functionality

## Architecture

### Data Flow

```
[VA CDW Mock Data]          (med-data: SQL Server CDWWork database)
        ↓
[ETL Pipeline]              (med-etl: Extract, Transform, Load)
        ↓
[Extract Database]          (med-etl: SQL Server Extract database)
        ↓
[AI/ML Processing]          (med-ml: JupyterLab notebooks, MinIO storage)
        ↓
[Web Dashboard]             (med-view: FastAPI + HTMX UI)
```

### Subsystem Interdependencies

1. **med-data** (Mock Data Service)
   - Provides SQL Server 2019 container with CDWWork database
   - Provides MinIO object storage for Parquet files
   - Generates sample extract files (ADM, CLI, DEM, LAB, RAD)
   - No dependencies on other subsystems

2. **med-etl** (Data Pipeline)
   - **Depends on**: med-data (requires CDWWork database and MinIO)
   - Reads from: CDWWork database and MinIO Parquet files
   - Writes to: Extract database and ASCII extract files
   - Interactive CLI for ETL operations

3. **med-ml** (AI/ML Layer)
   - **Status**: Active development - feature engineering complete, clustering in progress
   - **Dependencies**: MinIO object storage and CDWWork database from med-data
   - **Data Sources**:
     - Kaggle DDI reference data stored in MinIO
     - Patient medications from CDWWork database (RxOut, BCMA schemas)
     - Patient demographics from CDWWork database (SPatient schema)
   - **Current Progress**:
     - ✅ Data preparation (3 notebooks: DDI, medications, demographics)
     - ✅ Exploratory data analysis
     - ✅ Data cleaning and validation
     - ✅ Feature engineering (19 patient-level features)
     - 🔄 Patient risk clustering (in progress)
     - 🔜 Pattern analysis and predictive modeling
     - 🔜 PhysioNet MIMIC-IV integration for community care data (Phase 2)
   - **Tech Stack**: JupyterLab, Pandas, scikit-learn, PyArrow, MinIO, SQL Server
   - **Architecture**: Medallion pattern (v1_raw → v2_clean → v3_features → v4_models)
   - **Documentation**: Comprehensive guides for feature engineering, demographics, clustering, and PhysioNet integration

4. **med-view** (Web Dashboard)
   - **Status**: Early development stage
   - **Future dependency**: Extract database from med-etl and models from med-ml
   - Currently shows static mock data
   - FastAPI + HTMX + Jinja2 templates

### Database Architecture

**Source Database (CDWWork)** - Created by med-data
- Engine: SQL Server 2019
- Purpose: Mock VA Corporate Data Warehouse
- Schemas: Dim, Inpat, SPatient, SStaff, RxOut, BCMA
- 30+ tables with ~270-600+ sample records (expandable)
- **Patient Cohorts**: Expandable from 10 base → 15 (+elderly) → 25 (+expansion) patients
- **Medications**: 20-120+ outpatient prescriptions, 20-40+ BCMA administration events
- **DDI Testing**: 18-28+ clinically significant drug-drug interaction scenarios
- **Geographic Data**: 4 VA facilities (Sta3n 508-Atlanta, 516-Bay Pines, 552-Dayton, 688-Washington DC)
- **Mental Health**: Expansion cohort emphasizes mental health medications and interactions
- **Phase 2 Planning**: PhysioNet MIMIC-IV community care data integration (see med-ml)

**Target Database (Extract)** - Created by med-etl
- Engine: SQL Server 2019
- Purpose: Prepared data for downstream applications
- Schemas: Data
- Tables: Data.ADM, Data.LBB, Data.RAD, Data.CLI

Both databases run in the same Docker container but maintain logical separation.

### Python Module Organization

**med-etl modules** (src/ directory):
- `db_config.py` - Database connection management using pyodbc and .env prefixes
- `fetch_records.py` - Fetch data from CDWWork and MinIO sources
- `create_extracts.py` - Generate ASCII fixed-width extract files
- `input_validation.py` - User input validation for CLI
- `logging_config.py` - Application logging configuration
- `minio_config.py` - S3-compatible storage configuration
- `constants_*.py` - Schema definitions and SQL queries for each extract type

**med-data modules** (src/ directory):
- `create_sample_extract.py` - Generate sample ASCII extract files
- `constants_sample_extract.py` - Schema definitions for extract generation
- `csv_to_parquet.py` - Convert CSV to Parquet format for MinIO

**med-data SQL scripts** (sql-server/cdwwork/insert/):
- `_master.sql` - Master insert script for base patient cohort (10 patients)
- `add_elderly_patients.sql` - Incremental script for elderly cohort with DDI scenarios (+5 patients, 15 total)
- `add_expansion_patients.sql` - Incremental script for expansion cohort with mental health emphasis (+10 patients, 25 total)

**med-view structure**:
- `main.py` - FastAPI application entry point
- `templates/` - Jinja2 HTML templates
- `static/` - CSS, JavaScript, images

**med-ml structure** (src/ directory):
- `config.py` - Centralized MinIO and path configuration
- `ddi_transforms.py` - DDI-specific data transformations
- `01a_dataprep_ddi.ipynb` - DDI reference data preparation
- `01b_dataprep_medications.ipynb` - Patient medications preparation
- `01c_dataprep_demographics.ipynb` - Patient demographics preparation
- `02_explore.ipynb` - Exploratory data analysis
- `03_clean.ipynb` - Data cleaning and validation
- `04_features.ipynb` - Feature engineering (patient & DDI features)
- `05_clustering.ipynb` - Patient risk clustering (in progress)
- `06_analysis.ipynb` - Results analysis (pending)

**med-ml documentation**:
- `FEATURE_ENGINEERING_GUIDE.md` - Feature engineering methodology
- `DEMOGRAPHICS_IMPLEMENTATION.md` - Demographics integration details
- `CLUSTERING_AND_ANALYSIS_GUIDE.md` - Clustering strategy and analysis guide
- `PHYSIONET_INTEGRATION_GUIDE.md` - PhysioNet MIMIC-IV community care integration plan (Phase 2)

## Environment Configuration

### .env File Location
A single shared `.env` file is used by all subsystems (NOT in version control):
- `/Users/chuck/swdev/med/med-insight/.env` - Single shared configuration for all subsystems

All four subsystems (med-data, med-etl, med-ml, med-view) read from this root-level .env file. Python code in subsystems can load it using `python-dotenv` with the appropriate relative path to the root.

**Security**: Never commit the `.env` file. Obtain from peer developers.

**Simplicity**: Using a single shared .env file simplifies configuration management for solo development and avoids duplication.

### Key Environment Variables

**SQL Server** (used by med-data, med-etl):
- `MSSQL_SA_PASSWORD` - SQL Server sa account password
- `CDWWORK_DB_PASSWORD` - CDWWork database password (same as sa password)
- `EXTRACT_DB_PASSWORD` - Extract database password (same as sa password)

**MinIO** (used by med-data, med-etl, med-ml):
- `MINIO_ROOT_USER` - MinIO admin username
- `MINIO_ROOT_PASSWORD` - MinIO admin password
- `MINIO_ENDPOINT` - Host and port (localhost:9000)

**Note**: med-ml uses MinIO extensively for medallion architecture data storage (raw, clean, features, models)

**Database Connection Pattern** (med-etl):
The `db_config.py` module uses environment variable prefixes to support multiple databases:
- `CDWWORK_*` prefix for source database
- `EXTRACT_*` prefix for target database
- Usage: `create_connection("CDWWork")` or `create_connection("Extract")`

### Python Virtual Environments

**Root-level environment** (`/Users/chuck/swdev/med/med-insight/.venv`):
- Shared dependencies across subsystems
- Created via: `python3 -m venv .venv`
- Activate: `source .venv/bin/activate`

**Subsystem-specific environments** (optional):
Some subsystems may use their own `.venv` for isolation. Check subsystem README.

**Python Version**: Use Python 3.11.x (avoid 3.12+ due to venv quirks)

## Common Development Tasks

### Add New Extract Type to med-etl

1. Create SQL query constants: `src/constants_sql_<type>.py`
2. Create ASCII schema constants: `src/constants_ascii_<type>.py`
3. Add fetch logic to `src/fetch_records.py`
4. Add extract generation to `src/create_extracts.py`
5. Update input validation in `src/input_validation.py`
6. Test with sample data via `python main.py`

### Database Schema Changes

**For CDWWork (med-data)**:
1. Edit SQL scripts in `med-data/sql-server/cdwwork/create/`
2. Regenerate database: `cd create && ./_master.sh`
3. Repopulate base data: `cd ../insert && ./_master.sh`
4. Optional expansions:
   - Add elderly cohort (15 total): `sqlcmd ... -d CDWWork -i add_elderly_patients.sql`
   - Add expansion cohort (25 total): `sqlcmd ... -d CDWWork -i add_expansion_patients.sql`

**For Extract (med-etl)**:
1. Edit SQL scripts in `med-etl/dbscript/sql-server/extract/create/`
2. Regenerate database: `cd create && ./_master.sh`

### Managing Python Dependencies

```bash
# Install new package
pip install <package-name>

# Update requirements.txt
pip freeze > requirements.txt

# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### Container Management

```bash
# Start containers
docker start sqlserver2019 med-insight-minio

# Stop containers
docker stop sqlserver2019 med-insight-minio

# View container logs
docker logs sqlserver2019
docker logs med-insight-minio

# Restart containers
docker restart sqlserver2019 med-insight-minio

# Check container status
docker ps
```

## Project Conventions

### Code Style
- Python follows PEP 8 conventions
- Use descriptive variable names matching healthcare domain terminology
- Database column names use VA naming conventions (e.g., RxOutpatSID, PatientSID)

### File Naming
- Python modules: lowercase with underscores (`db_config.py`)
- SQL scripts: lowercase with underscores (`db_database.sql`)
- Constants modules: prefix with `constants_` (`constants_sql_adm.py`)
- Master scripts: prefix with `_master` (`_master.sh`, `_master.sql`)

### Database Naming
- Schemas: PascalCase (`Inpat`, `SPatient`, `RxOut`)
- Tables: PascalCase (`RxOutpat`, `BCMAMedicationLog`)
- Columns: PascalCase with suffixes (`RxOutpatSID`, `PatientICN`)

### Git Workflow
- **Branch**: `main` (no separate development branch currently)
- **Issues**: GitHub Issues used to track development work
- **Commits**: Descriptive messages focusing on "why" rather than "what"

## Platform-Specific Notes

### macOS Setup (Primary Platform)
- Use Homebrew for package management
- Docker Desktop recommended over Podman
- SQL Server runs via Rosetta 2 on Apple Silicon (M1/M2/M3)
- Verify Rosetta 2 installed: `pgrep -q oahd && echo "Installed" || echo "NOT installed"`

### Container Platform
- **Docker Desktop**: Recommended, includes GUI, auto-starts on login
- **Podman**: Alternative, lightweight, requires `podman machine start` per session

### ODBC Drivers
Required for Python pyodbc connectivity to SQL Server:
- Install via: `brew install msodbcsql18 unixodbc`
- Verify: `odbcinst -q -d` (should show "ODBC Driver 18 for SQL Server")

## Troubleshooting

### Container Issues
```bash
# If containers won't start
docker ps -a  # Check container status
docker logs sqlserver2019  # Check SQL Server logs

# If port 1433 already in use
lsof -i :1433  # Find process using port
```

### Database Connection Issues
```bash
# Test SQL Server connectivity
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT @@VERSION"

# Check ODBC drivers installed
odbcinst -q -d
```

### Python Import Errors
```bash
# Verify virtual environment activated (prompt shows (.venv))
which python  # Should point to .venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### MinIO Access Issues
- Console: http://localhost:9001 (login with MINIO_ROOT_USER/MINIO_ROOT_PASSWORD)
- API: http://localhost:9000 (S3-compatible endpoint)
- Verify container running: `docker ps | grep minio`

## Additional Resources

- **Project Lead**: Chuck Sylvester (contact for .env files and setup assistance)
- **GitHub Issues**: Track development tasks and bugs
- **Subsystem READMEs**: Detailed setup instructions for each component
  - `med-data/README.md` - Comprehensive setup guide with expandable patient cohort documentation
  - `med-etl/README.md` - ETL pipeline setup and configuration
  - `med-ml/README.md` - AI/ML layer with DDI risk analysis (feature engineering complete, clustering in progress)
  - `med-view/README.md` - Web dashboard setup (early stage)
- **med-ml Methodology Guides**: Comprehensive technical documentation
  - `FEATURE_ENGINEERING_GUIDE.md` - Feature engineering approach for DDI risk analysis
  - `DEMOGRAPHICS_IMPLEMENTATION.md` - Patient demographics integration details
  - `CLUSTERING_AND_ANALYSIS_GUIDE.md` - Patient risk clustering strategy and analysis methodology
  - `PHYSIONET_INTEGRATION_GUIDE.md` - PhysioNet MIMIC-IV community care integration plan (Phase 2)
