# med-data

Mock Data Service for VA Healthcare Analytics Development

## Overview

**med-data** is a standalone application that supports other applications within the "med" family of software products. It provides a mock data service that simulates patient, medical treatment, and other supporting data in formats compatible with:

- **VA Corporate Data Warehouse (CDW)** - Microsoft SQL Server 2019 data source
- **VA Summit Data Platform (SDP)** - Azure Data Lake Storage Gen2 (ADLS Gen2) with Parquet files
- **Legacy Extract Files** - ASCII fixed-length clinical data files matching mainframe/SAS formats

The data available within med-data is **synthetic** and does not contain PHI or PII. It supports local development, testing, and demonstration of med family applications.

### Key Features

- **SQL Server Database**: Simulates VA CDW with 6 schemas, 30+ tables
- **MinIO Object Storage**: Mimics ADLS Gen2 for Parquet file storage
- **Sample Extract Generator**: Creates fixed-length ASCII clinical data files
- **Pharmacy Data**: Outpatient prescriptions (RxOut) and inpatient medication administration (BCMA)
- **Realistic Test Data**: 10 patients, 6 providers, 20 prescriptions, 20 BCMA events, 8 inpatient stays

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Detailed Setup](#detailed-setup)
  - [Getting Started](#getting-started)
  - [Install Required Tools](#install-required-tools)
  - [Container Infrastructure](#container-infrastructure)
  - [SQL Server Setup](#sql-server-setup)
  - [Database Loading](#database-loading)
  - [Database Structure Overview](#database-structure-overview)
  - [Verification Steps](#verification-steps)
  - [MinIO Setup](#minio-setup)
  - [Python Environment](#python-environment)
- [Database Schemas and Data Domains](#database-schemas-and-data-domains)
- [Sample Extract Generation](#sample-extract-generation)
- [Environment Configuration](#environment-configuration-env)
- [Daily Development Workflow](#daily-development-workflow)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## Prerequisites

Before starting, ensure you have the following:

### Required Software
- [ ] **macOS** (these instructions are Mac-specific; adjust for Windows/Linux)
- [ ] **Xcode Command Line Tools** (includes git and other essential developer utilities)
- [ ] **Homebrew** package manager ([install](https://brew.sh))
- [ ] **Docker Desktop** (recommended) or **Podman** as alternative
- [ ] **Python 3.11** (avoid 3.12+ due to venv quirks)
- [ ] **Terminal** application
- [ ] **VS Code** with [mssql extension](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) (recommended for database work)

### Apple Silicon Mac Requirements

If you have an Apple Silicon Mac (M1, M2, M3, or later), you need **Rosetta 2** to run x86/Intel-based containers. SQL Server 2019 runs as a Linux x86_64 container and requires Rosetta 2 for emulation on ARM-based Macs.

**Check if Rosetta 2 is already installed**:

```bash
# Check for Rosetta 2
pgrep -q oahd && echo "Rosetta 2 is installed" || echo "Rosetta 2 is NOT installed"
```

**Install Rosetta 2** (if not already installed):

```bash
softwareupdate --install-rosetta
```

You'll be prompted to agree to the license agreement. Press `A` to agree and complete the installation.

**Alternative installation method** (if the command above doesn't work):

```bash
softwareupdate --install-rosetta --agree-to-license
```

**Note**: Rosetta 2 installation is quick (typically 1-2 minutes) and only needs to be done once per system. Intel-based Macs do not require Rosetta 2.

**Verify your Mac architecture**:

```bash
uname -m
# Output: "arm64" = Apple Silicon, "x86_64" = Intel
```

### Required Files
- [ ] **`.env` file** - Obtain from peer developer (contains passwords)

### System Requirements
- **Disk Space**: ~10 GB for containers and data
- **RAM**: 8 GB minimum, 16 GB recommended
- **Ports**: 1433 (SQL Server), 9000-9001 (MinIO) must be available

### Time Estimate
- **First-time setup**: 45-60 minutes
- **Daily startup**: 2-3 minutes

---

## Detailed Setup

This section provides step-by-step instructions for first-time setup of the med-data development environment. Follow these steps in order for the smoothest setup experience.

---

### Getting Started

Before installing tools and containers, you need to obtain the project files and configuration.

#### Clone the Repository

Navigate to your development directory and clone the repository:

```bash
cd ~/swdev/med
git clone <repository-url> med-data
cd med-data
```

**Note**: Replace `<repository-url>` with the actual repository URL provided by your team lead.

**Git Configuration**: Before making your first commit, configure git with your identity and preferred settings:

```bash
# Set your name (appears in commit history)
git config --global user.name "Your Full Name"

# Set your email (appears in commit history)
git config --global user.email "your.email@example.com"

# Enable colored output for better readability
git config --global color.ui auto
```

**Verify your configuration**:
```bash
git config --global --list
```

These settings are stored globally in `~/.gitconfig` and apply to all git repositories on your system.

#### Obtain .env File

The `.env` file contains passwords and configuration required for SQL Server and MinIO.

1. **Request .env file** from a peer developer or team lead
2. **Place in project root**: `/Users/<username>/swdev/med/med-data/.env`
3. **Verify placement**:
   ```bash
   ls -la .env
   ```

**Security Note**: The `.env` file is excluded from version control (already in `.gitignore`). Never commit passwords to the repository.

#### Verify Project Directory

Confirm you're in the correct location:

```bash
pwd
# Expected output: ~/swdev/med/med-data

ls
# You should see: README.md, CLAUDE.md, sql-server/, src/, requirements.txt, etc.
```

---

### Install Required Tools

Install all required software tools before proceeding with container and database setup.

#### Install Xcode Command Line Tools

The Xcode Command Line Tools provide essential developer utilities including `git`, `make`, and compilers. **Note**: You do not need to install the full Xcode application—the command line tools are sufficient.

**Check if already installed**:

```bash
xcode-select -p
```

If installed, this will display the path (typically `/Library/Developer/CommandLineTools`).

**Install the Command Line Tools**:

```bash
xcode-select --install
```

This will open a dialog box asking you to install the tools. Click "Install" and follow the prompts. The installation takes approximately 5-10 minutes.

**Verify installation**:

```bash
# Check Xcode Command Line Tools
xcode-select -p

# Verify git is available
git --version
# Expected output: git version 2.x.x
```

#### Install Homebrew (if needed)

Homebrew is a package manager for macOS. Check if already installed:

```bash
brew --version
```

If not installed, install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the post-installation instructions to add Homebrew to your PATH.

#### Install Python 3.11

**Recommended Version**: Python 3.11.x (avoid 3.12+ due to virtual environment quirks)

Check your current Python version:

```bash
python3 --version
```

If you don't have Python 3.11.x, install it:

```bash
brew install python@3.11
```

After installation, you may need to add Python 3.11 to your PATH. Homebrew will provide instructions, typically:

```bash
# Add to ~/.zshrc or ~/.bash_profile
echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Verify Installation**:
```bash
python3 --version  # Should show 3.11.x
pip3 --version     # Should show 24.x or 25.x
```

#### Install SQL Server Command-Line Tools

Install the Microsoft SQL Server tools for database connectivity and management:

```bash
# Add Microsoft repository
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update

# Install SQL Server tools and ODBC drivers
brew install mssql-tools msodbcsql18

# Install unixODBC driver manager (required for Python pyodbc)
brew install unixodbc
```

**Add sqlcmd to PATH** (add to `~/.zshrc` or `~/.bash_profile`):

```bash
echo 'export PATH="/usr/local/opt/mssql-tools/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Verify Installation**:

```bash
# Test sqlcmd
sqlcmd '-?'

# Verify ODBC drivers
odbcinst -q -d
# Should see: [ODBC Driver 18 for SQL Server]
```

#### Install Docker Desktop (Recommended)

**Docker Desktop** is the recommended container runtime for most developers.

**Download and Install**:

1. Download from [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Choose "Apple Chip" or "Intel Chip" based on your Mac
3. Open the `.dmg` file and drag Docker to Applications folder
4. Launch Docker Desktop from Applications
5. Complete the setup wizard
6. Add Docker to your dock for easy access

**Configure Docker Desktop** (optional):

1. Open Docker Desktop preferences
2. Go to Settings → General
3. Enable "Start Docker Desktop when you log in" for convenience
4. Allocate resources (recommended: 4 CPUs, 8 GB RAM)

**Verify Installation**:

```bash
docker --version
# Expected output: Docker version 24.x.x or later
```

#### Alternative: Install Podman

**Podman** is a lightweight, daemon-free alternative to Docker Desktop.

**Install Podman**:

```bash
brew install podman
```

**Initialize Podman VM** (one-time setup):

```bash
podman machine init --cpus 4 --memory 8192 --disk-size 40
```

Configuration details:
- `--cpus 4`: Allocate 4 CPU cores
- `--memory 8192`: Allocate 8 GB RAM
- `--disk-size 40`: Allocate 40 GB disk space

**Verify Installation**:

```bash
podman --version
# Expected output: podman version 4.x.x or later
```

**Note**: If using Podman, you'll need to run `podman machine start` at the beginning of each development session.

---

### Container Infrastructure

This project uses containers to run SQL Server and MinIO. **Docker Desktop** is the recommended option for most developers due to its ease of use and wide adoption. Podman is available as a lightweight, daemon-free alternative.

**Primary Recommendation**: Docker Desktop (easier setup, better tooling integration)
**Alternative**: Podman (lighter weight, no background daemon required)

#### Start Container Runtime

**Using Docker Desktop**:

- Click Docker icon in Applications or dock
- Wait for "Docker Desktop is running" status in menu bar
- The application will run in the background

**Using Podman**:

```bash
# Start Podman VM (required at beginning of each session)
podman machine start
```

**Verify Container Runtime**:

```bash
# Docker Desktop
docker ps
# Should show column headers (may be empty if no containers running yet)

# Podman
podman ps
# Should show column headers (may be empty if no containers running yet)
```

---

### SQL Server Setup

#### Pull and Create SQL Server Container

**Important**: Use SQL Server **2019**, not 2022. SQL Server 2022 has issues on Apple Silicon.

##### Using Docker:

```bash
# Pull image
docker pull mcr.microsoft.com/mssql/server:2019-latest

# Create and run container (FIRST TIME ONLY)
docker run --platform linux/amd64 \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=YourSecurePassword123!' \
  -p 1433:1433 \
  --name sqlserver2019 \
  -d mcr.microsoft.com/mssql/server:2019-latest
```

**Password Requirements**: 8+ characters with uppercase, lowercase, numbers, and special characters.

##### Using Podman:

```bash
# Create and run container (FIRST TIME ONLY)
podman run -d \
  --platform=linux/amd64 \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=YourSecurePassword123!' \
  -p 1433:1433 \
  --name sqlserver2019 \
  mcr.microsoft.com/mssql/server:2019-latest
```

#### Start/Stop SQL Server Container

**Start (daily use):**
```bash
# Docker
docker start sqlserver2019

# Podman
podman start sqlserver2019
```

**Stop:**
```bash
# Docker
docker stop sqlserver2019

# Podman
podman stop sqlserver2019
```

**Check Status:**
```bash
# Docker
docker ps

# Podman
podman ps
```

---

### Database Loading

#### Load Database Using Master Scripts

The database is loaded in two phases:

**Phase 1: Create Database Structure**
```bash
cd ~/swdev/med/med-data/sql-server/cdwwork/create
./_master.sh
```

This creates:
- `CDWWork` database
- 6 schemas (Dim, Inpat, SPatient, SStaff, RxOut, BCMA)
- 30+ tables

**Phase 2: Insert Sample Data**
```bash
cd ../insert
./_master.sh
```

This populates all tables with realistic test data.

**Note**: The `_master.sh` scripts use the `MSSQL_SA_PASSWORD` environment variable from your `.env` file.

#### Alternative: Manual sqlcmd Execution

If you prefer to run manually:

```bash
cd sql-server/cdwwork/create
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -i _master.sql

cd ../insert
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -i _master.sql
```

#### Alternative: Using VS Code with mssql Extension

**Prerequisites**: Install the [mssql extension](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) for VS Code.

1. **Create Connection:**
   - Open Command Palette (Cmd+Shift+P)
   - Type "MSSQL: Connect" and select it
   - Choose "Create Connection Profile"
   - Profile Name: `sqlserver19-local`
   - Server: `127.0.0.1,1433` (note the **comma**)
   - Database: Leave blank or enter `CDWWork`
   - Authentication: SQL Login
   - Username: `sa`
   - Password: (from your .env file)
   - Trust server certificate: `yes`
   - Save password: `yes`

2. **Run Scripts:**
   - Navigate to `sql-server/cdwwork/create/`
   - Open `_master.sql`
   - Right-click in editor and select "Execute Query" (or press Cmd+Shift+E)
   - Navigate to `sql-server/cdwwork/insert/`
   - Open and execute `_master.sql`

**Important**: The `db_database.sql` script includes `DROP DATABASE` - use this to start fresh.

---

### Database Structure Overview

The **CDWWork** database simulates VA Corporate Data Warehouse structure with 6 schemas:

| Schema | Purpose | Tables | Sample Records |
|--------|---------|--------|----------------|
| **Dim** | Dimension/reference data | 7 | States, divisions, ward locations |
| **Inpat** | Inpatient admissions | 3 | 8 inpatient stays |
| **SPatient** | Patient demographics | 4 | 10 test patients |
| **SStaff** | Staff/providers | 2 | 6 providers |
| **RxOut** | Pharmacy outpatient | 4 | 20 prescriptions, 31 fills |
| **BCMA** | Medication administration | 4 | 20 administration events |

**Total Tables**: 30+
**Total Records**: ~200+ across all tables

See **[CLAUDE.md](CLAUDE.md)** for detailed schema documentation, relationships, and sample queries.

---

### Verification Steps

After completing the setup, verify everything works correctly.

#### 1. Verify SQL Server Connection

```bash
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -Q "SELECT @@VERSION"
```

**Expected output**: Microsoft SQL Server 2019 version information

#### 2. Verify Database and Schemas

```bash
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -d CDWWork -Q "
SELECT name AS SchemaName FROM sys.schemas
WHERE name IN ('Dim', 'Inpat', 'SPatient', 'SStaff', 'RxOut', 'BCMA')
ORDER BY name"
```

**Expected output**: All 6 schemas listed

#### 3. Verify Sample Data Loaded

```bash
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -d CDWWork -Q "
SELECT 'RxOut.RxOutpat' AS TableName, COUNT(*) AS RecordCount FROM RxOut.RxOutpat
UNION ALL
SELECT 'RxOut.RxOutpatFill', COUNT(*) FROM RxOut.RxOutpatFill
UNION ALL
SELECT 'BCMA.BCMAMedicationLog', COUNT(*) FROM BCMA.BCMAMedicationLog
UNION ALL
SELECT 'SPatient.SPatient', COUNT(*) FROM SPatient.SPatient"
```

**Expected output**:
```
TableName                 RecordCount
RxOut.RxOutpat           20
RxOut.RxOutpatFill       31
BCMA.BCMAMedicationLog   20
SPatient.SPatient        10
```

#### 4. Verify Table Relationships

```bash
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -d CDWWork -Q "
SELECT p.DrugNameWithDose, COUNT(f.RxOutpatFillSID) AS FillCount
FROM RxOut.RxOutpat p
LEFT JOIN RxOut.RxOutpatFill f ON p.RxOutpatSID = f.RxOutpatSID
GROUP BY p.DrugNameWithDose
ORDER BY FillCount DESC"
```

This should show prescriptions with their fill counts, demonstrating proper relationships.

---

### MinIO Setup

MinIO simulates Azure Data Lake Storage Gen2 for Parquet file storage.

#### Create and Run MinIO Container

##### Using Docker:

```bash
# Create storage directory first
mkdir -p ~/minio-data

# Run MinIO container
docker run -d --name med-insight-minio \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD='YourMinIOPassword123!' \
  -v $HOME/minio-data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

##### Using Podman:

```bash
# Create storage directory
mkdir -p ~/minio-data

# Run container
podman run -d --name med-insight-minio \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD='YourMinIOPassword123!' \
  -v "$HOME/minio-data:/data" \
  minio/minio server /data --console-address ":9001"
```

#### Access MinIO Console
```text
MinIO Console:  http://localhost:9001  
MinIO API (S3): http://localhost:9000  
```
**Login Credentials**:
- Username: `admin`
- Password: (from your .env file)

#### Create Buckets and Folder Structure

MinIO uses **buckets** (equivalent to ADLS Gen2 containers) to organize data.

**Primary bucket**: `ci-published` (simulates VA SDP container)

**Folder structure**:
```
ci-published/
 └─ vista/
     └─ current/
         ├─ outpat/
         │   └─ visit/
         │       └─ visitdatetime_year=2025/
         │           └─ visitdatetime_quarter=20251/
         ├─ spatient/
         │   ├─ spatient/
         │   └─ spatientaddress/
         └─ sstaff/
             └─ sstaff/
```

**Workflow**:

1. Create bucket via MinIO Console (one time action)  
2. Create folder hierarchy for initial path
3. Upload Parquet files into newly created path/folder
    - converted from CSV using `csv_to_parquet.py`
4. Repeat steps 2 and 3 for remaining paths

---

### Python Environment

Python is used for sample extract generation and CSV-to-Parquet conversion. This section covers setting up the Python virtual environment and installing project dependencies.

**Prerequisites**: Python 3.11.x should already be installed from the [Install Required Tools](#install-required-tools) section.

#### Create Python Virtual Environment

```bash
cd ~/swdev/med/med-data
python3 -m venv .venv
```

The `.venv` directory name keeps the environment hidden but discoverable.

#### Activate Virtual Environment

**macOS/Linux**:
```bash
source .venv/bin/activate
```

**Windows**:
```text
Command:  .venv\Scripts\activate

Git Bash: .venv/Scripts/Activate
```

After activation, your prompt shows `(.venv)` and you can use `python` instead of `python3`.

#### Install Dependencies

```bash
pip install -r requirements.txt
```

**Key dependencies installed**:
- `pyodbc` - SQL Server connectivity
- `pandas`, `pyarrow` - Parquet file handling
- `boto3`, `s3fs` - S3-compatible storage (MinIO)
- `polars`, `fastparquet` - Alternative data processing

#### Verify ODBC Drivers for Python

The ODBC drivers required for Python's `pyodbc` library should already be installed from the [Install Required Tools](#install-required-tools) section.

**Verify driver installation**:
```bash
odbcinst -q -d
```

You should see: `[ODBC Driver 18 for SQL Server]`

If the ODBC driver is not installed, return to the [Install Required Tools](#install-required-tools) section and complete the SQL Server Command-Line Tools installation.

#### Deactivate Virtual Environment

When done working:
```bash
deactivate
```

#### Update requirements.txt (Maintenance)

After installing new packages via pip:
```bash
pip freeze > requirements.txt
```

---

### Detailed Documentation

For comprehensive schema documentation, table relationships, and sample queries, see **[CLAUDE.md](CLAUDE.md)**.

---

## Sample Extract Generation

The `src/` directory contains Python utilities to generate ASCII fixed-length clinical data files.

### Purpose

Sample extract files simulate legacy mainframe/SAS data formats used in healthcare analytics. These files are used for:

1. **Development**: Test ETL pipelines with realistic data
2. **Integration Testing**: Validate data processing logic
3. **Documentation**: Provide schema specifications
4. **Prototyping**: Enable rapid feature development

### Key Programs

**`create_sample_extract.py`**
Main program that generates sample extract files with realistic clinical data.

**`constants_sample_extract.py`**
Configuration constants and schema definitions.

**`csv_to_parquet.py`**
Utility to convert CSV files to Parquet format for MinIO upload.

### Supported Data Types

Currently 5 of 15 planned data types are implemented:

- **ADM** - Hospital admission data (demographics, admissions, diagnosis codes)
- **CLI** - Clinical/clinic visit data (appointments, procedures, providers)
- **DEM** - Demographics data (patient info, eligibility, veteran status)
- **LAB** - Laboratory test data (results, specimen info, reference ranges)
- **RAD** - Radiology exam data (imaging studies, reports, modalities)

### Usage Examples

**Generate all extract files**:
```bash
cd ~/swdev/med/med-data
source .venv/bin/activate
python src/create_sample_extract.py
```

**Output location**: Creates timestamped directory `extract_files_YYYYMMDD_HHMMSS/`

**Create specific extract with custom record count**:
```python
from src.create_sample_extract import create_sample_extract_file
create_sample_extract_file('ADM', 'admission_data.txt', 50)
```

**View schema for a data type**:
```python
from src.create_sample_extract import print_schema_info
print_schema_info('RAD')
```

**View all available schemas**:
```python
from src.create_sample_extract import print_all_schemas
print_all_schemas()
```

### Generated Files

```
extract_files_YYYYMMDD_HHMMSS/
├── extract_schemas.txt    # Technical schema documentation
├── adm_extract.txt        # Hospital admission data
├── cli_extract.txt        # Clinical/clinic visit data
├── dem_extract.txt        # Demographics data
├── lab_extract.txt        # Laboratory test data
└── rad_extract.txt        # Radiology exam data
```

### File Format Features

- Fixed-width ASCII text files with header rows
- SAS-compatible column names (ALL_CAPS with underscores)
- Proper field justification (left/right) and padding (spaces/zeros)
- Header truncation when column names exceed field width
- Consistent record lengths per data type

### CSV to Parquet Conversion

After generating CSV files, convert to Parquet for MinIO:

```bash
python src/csv_to_parquet.py
```

Edit the file to uncomment the section for the data type you want to convert.

---

## Environment Configuration (.env)

This project uses environment variables for sensitive configuration.

### Setup Instructions

1. **Obtain .env file** from peer developer (contains passwords)
2. **Place in project root**: `/Users/chuck/swdev/med/med-data/.env`
3. **Never commit to version control** (already in .gitignore)

### Required Variables

Create a `.env` file in the project root with the following content:

```bash
# SQL Server Configuration
MSSQL_SA_PASSWORD=YourSecurePassword123!

# MinIO Configuration
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=YourMinIOPassword123!

# Python/Application Configuration
DEFAULT_OUTPUT_DIR=/Users/chuck/swdev/med/med-output/sample/dssext
```

### Creating .env.example Template

To create a template for other developers:

```bash
# Copy your .env
cp .env .env.example

# Edit .env.example and replace actual values with placeholders
# Example:
# MSSQL_SA_PASSWORD=<your-strong-password-here>
# MINIO_ROOT_PASSWORD=<your-minio-password-here>
```

### Using Environment Variables in Scripts

The `_master.sh` scripts automatically source the `.env` file:

```bash
#!/bin/bash
# Load environment variables
source ../../.env

# Use variable
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -i _master.sql
```

---

## Daily Development Workflow

### Starting Your Development Session

**Using Docker Desktop** (recommended):

```bash
# 1. Start Docker Desktop
# Open Docker Desktop app (or it may auto-start on login)

# 2. Start containers
docker start sqlserver2019 med-insight-minio

# 3. Verify containers running
docker ps

# 4. Activate Python environment (if needed)
cd ~/swdev/med/med-data
source .venv/bin/activate

# 5. Verify SQL Server connectivity
sqlcmd -S 127.0.0.1,1433 -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT @@VERSION"
```

**Using Podman** (alternative):

```bash
# 1. Start Podman VM first
podman machine start

# 2. Start containers
podman start sqlserver2019 med-insight-minio

# 3. Verify containers running
podman ps

# 4-5. Same as Docker Desktop workflow above
```

### Ending Your Development Session

**Using Docker Desktop**:

```bash
# 1. Deactivate Python environment (if active)
deactivate

# 2. Stop containers (optional - Docker Desktop can keep them running)
docker stop sqlserver2019 med-insight-minio

# 3. Quit Docker Desktop (optional - can leave running in background)
# Click Docker icon in menu bar → Quit Docker Desktop
```

**Using Podman**:

```bash
# 1. Deactivate Python environment (if active)
deactivate

# 2. Stop containers
podman stop sqlserver2019 med-insight-minio

# 3. Stop Podman VM
podman machine stop
```

**View container logs**:
```bash
# Docker Desktop
docker logs sqlserver2019
docker logs med-insight-minio

# Podman (alternative)
podman logs sqlserver2019
podman logs med-insight-minio
```

---

## Project Structure

```
med-data/
├── adls-gen2/                         # MinIO object storage structure
│   ├── ci-published/                  # Production-like bucket
│   │   └── vista/current/             # VistA current data
│   │       ├── outpat/visit/          # Outpatient visits
│   │       ├── spatient/spatient/     # Patient data
│   │       └── sstaff/sstaff/         # Staff data
│   └── med-sandbox/                   # Sandbox/testing bucket
│       └── extract-file/              # Extract files (CSV/Parquet)
│           ├── lbb/                   # Lab results
│           └── rad/                   # Radiology
├── sql-server/                        # MS SQL Server setup structure
│   └── cdwwork/                       # CDW cdwork database
│       ├── create/                    # Table creation scripts
│       └── insert/                    # Data population scripts
├── src/                               # Python utilities
│   ├── create_sample_extract.py       # Extract file generator
│   ├── constants_sample_extract.py    # Schema definitions
│   └── csv_to_parquet.py              # CSV to Parquet converter
├── .env                               # Environment variables (NOT in git)
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── README.md                          # This file (setup and reference)
└── CLAUDE.md                          # Detailed schema documentation
```
