# Med-View Subsystem Assessment & Recommendations

**Assessment Date**: December 2, 2025
**Assessed By**: Claude (Sonnet 4.5)
**Project**: Med-Insight DDI Risk Analysis Dashboard

---

## Executive Summary

You've built a **solid foundation** for a modern web dashboard using FastAPI + HTMX + Jinja2. The current implementation demonstrates clean architecture, good UI/UX patterns, and proper separation of concerns. However, it's currently a **technology demonstration** with placeholder data. To transform it into a **DDI Risk Dashboard**, you'll need to add data integration, domain-specific features, and analytical visualizations.

---

## Part 1: Current State Analysis

### ✅ **What's Working Well**

#### **1. Architecture & Tech Stack**
- **Clean FastAPI structure**: Well-organized routes, proper templating setup
- **Server-side rendering**: Fast initial page loads, SEO-friendly
- **HTMX integration**: Demonstrates partial page updates (`/time` endpoint)
- **Static file serving**: Properly configured for CSS/JS/images
- **Jinja2 templating**: Good use of template inheritance (`base.html` → child templates)

#### **2. UI/UX Quality**
- **Professional design**: Modern, clean aesthetic with good color scheme
- **Responsive layout**: Grid system adapts to screen sizes
- **Component library**: Cards, panels, buttons, tables, status pills
- **Sidebar navigation**: Collapsible with keyboard shortcut (Cmd+B)
- **Consistent styling**: Cohesive visual language throughout

#### **3. Code Quality**
- **Well-documented**: Clear comments in `main.py`
- **Semantic HTML**: Proper use of `<section>`, `<article>`, `<header>`
- **CSS organization**: Logical structure (reset → layout → components → responsive)
- **JavaScript modularity**: Clean event handling, no jQuery dependency
- **Accessibility**: ARIA labels on interactive elements

### ⚠️ **Current Limitations**

#### **1. No Data Integration**
- ❌ No database connections (SQL Server, MinIO)
- ❌ All data is hardcoded in `main.py` (lines 38-48)
- ❌ No connection to med-ml analytical outputs
- ❌ No `.env` configuration for credentials

#### **2. Placeholder Functionality**
- ❌ Timer/HTMX pages are demos, not domain-relevant
- ❌ "Datasets", "Alerts", "Settings" sidebar links go nowhere (`href="#"`)
- ❌ Topbar buttons ("Download Report", "Run Pipeline") are non-functional
- ❌ No actual DDI, patient, or medication data displayed

#### **3. Missing Core Features**
- ❌ No data visualization (charts, graphs)
- ❌ No search/filter capabilities
- ❌ No patient detail views
- ❌ No DDI risk scoring displays
- ❌ No "Blind Spot" concurrent care analysis

#### **4. Missing Infrastructure**
- ❌ No requirements.txt (dependencies not defined)
- ❌ No configuration management (database connections)
- ❌ No data access layer (services/repositories)
- ❌ No error handling
- ❌ No logging configuration

---

## Part 2: Gap Analysis for DDI Dashboard

To transform med-view into a **DDI Risk Analysis Dashboard**, you need:

### **Missing Layers**

```
Current:
┌─────────────────────────────┐
│  Presentation (Templates)   │ ✅ Exists
├─────────────────────────────┤
│  Routes/Controllers         │ ✅ Exists (minimal)
└─────────────────────────────┘

Needed:
┌─────────────────────────────┐
│  Presentation (Templates)   │ ✅ Exists → Needs DDI-specific views
├─────────────────────────────┤
│  Routes/Controllers         │ ✅ Exists → Needs DDI endpoints
├─────────────────────────────┤
│  Services/Business Logic    │ ❌ MISSING → Add DDI scoring, filtering
├─────────────────────────────┤
│  Data Access Layer (DAL)    │ ❌ MISSING → Add Parquet/SQL readers
├─────────────────────────────┤
│  Configuration              │ ❌ MISSING → Add .env, config.py
└─────────────────────────────┘
```

### **Missing Domain Features**

| Feature | Current | Needed |
|---------|---------|--------|
| **Patient Risk Overview** | Generic cards | 3 cluster tiles with real counts |
| **DDI Pair Explorer** | None | Searchable table of 71 DDI pairs |
| **Patient List** | None | Filterable table of 25 patients |
| **Patient Detail** | None | Med timeline + DDI alerts |
| **Blind Spot Detection** | None | Concurrent VA+Community DDI visualization |
| **High-Risk Alerts** | Generic "2 alerts" | Top 10 high-risk patients |
| **Charts/Graphs** | None | Plotly/Chart.js visualizations |

---

## Part 3: Recommended Architecture

### **Proposed Structure**

```
med-view/
├── main.py                          # FastAPI app entry point
├── config.py                        # Configuration (NEW)
├── requirements.txt                 # Dependencies (NEW)
├── .env                            # Secrets (NEW, not in git)
│
├── services/                        # Business logic (NEW)
│   ├── __init__.py
│   ├── ddi_service.py              # DDI risk calculations
│   ├── patient_service.py          # Patient data operations
│   └── cluster_service.py          # Clustering analysis
│
├── data/                            # Data access layer (NEW)
│   ├── __init__.py
│   ├── parquet_reader.py           # MinIO Parquet access
│   ├── sql_reader.py               # SQL Server access
│   └── cache.py                    # Optional: in-memory caching
│
├── routes/                          # Route handlers (NEW, refactor from main.py)
│   ├── __init__.py
│   ├── dashboard.py                # Overview, alerts
│   ├── patients.py                 # Patient list, detail
│   ├── ddi.py                      # DDI exploration
│   └── api.py                      # JSON endpoints for HTMX
│
├── static/
│   ├── styles.css                  # ✅ Keep
│   ├── app.js                      # ✅ Keep
│   ├── charts.js                   # Visualization helpers (NEW)
│   └── images/
│
└── templates/
    ├── base.html                   # ✅ Keep
    ├── dashboard/                  # DDI dashboard views (NEW)
    │   ├── overview.html           # Replace current index.html
    │   ├── clusters.html           # Risk cluster visualization
    │   └── blind_spot.html         # Concurrent care DDI
    ├── patients/                   # Patient views (NEW)
    │   ├── list.html
    │   └── detail.html
    ├── ddi/                        # DDI views (NEW)
    │   └── explorer.html
    └── partials/                   # ✅ Keep + expand
        ├── patient_card.html       # (NEW)
        ├── ddi_table.html          # (NEW)
        └── risk_chart.html         # (NEW)
```

---

## Part 4: Implementation Roadmap

### **Phase 1: Infrastructure (Week 1)**

**Goal**: Connect to data sources and set up configuration

#### **Tasks**:

**1. Create `requirements.txt`**:
```
fastapi
uvicorn[standard]
jinja2
python-multipart
python-dotenv
pyodbc           # SQL Server
s3fs             # MinIO
pandas
pyarrow
plotly           # Visualizations
```

**2. Create `.env` file**:
```bash
# MinIO (from med-ml)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=<secret>

# SQL Server (from med-data)
SQLSERVER_SERVER=127.0.0.1,1433
CDWWORK_DB_PASSWORD=<password>
```

**3. Create `config.py`**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
DEST_BUCKET = "med-data"

# SQL Server Configuration
SQLSERVER_SERVER = os.getenv("SQLSERVER_SERVER")
CDWWORK_DB_PASSWORD = os.getenv("CDWWORK_DB_PASSWORD")
```

**4. Create `data/parquet_reader.py`**:
```python
import pandas as pd
import s3fs
from config import *

class ParquetReader:
    def __init__(self):
        self.s3 = s3fs.S3FileSystem(...)

    def get_patient_features(self):
        """Load clustered patient features from med-ml"""
        path = f's3://{DEST_BUCKET}/v3_features/ddi/patients_features_clustered.parquet'
        with self.s3.open(path, 'rb') as f:
            return pd.read_parquet(f)

    def get_ddi_pairs(self):
        """Load DDI pairs from med-ml"""
        path = f's3://{DEST_BUCKET}/v3_features/ddi/ddi_pairs_features.parquet'
        ...
```

**5. Create `data/sql_reader.py`**:
```python
import pyodbc
import pandas as pd
from config import *

class SQLReader:
    def get_patient_demographics(self):
        """Get patient demographics from CDWWork"""
        conn = pyodbc.connect(...)
        query = "SELECT * FROM SPatient.SPatient"
        return pd.read_sql(query, conn)
```

**Deliverable**: Working data connections, ability to read med-ml outputs

---

### **Phase 2: Core Dashboard (Week 2)**

**Goal**: Build patient risk overview and cluster visualization

#### **Tasks**:

**1. Replace `index.html` with DDI-focused dashboard**:
   - 4 metric cards:
     - **Total Patients**: 25
     - **High-Risk Patients**: Count from cluster 0
     - **DDI Pairs Detected**: 71
     - **Concurrent Care Patients**: 10

   - **Cluster tiles** (3 clusters from med-ml):
     ```
     ┌───────────────────────────────────────────┐
     │ 🔴 High-Risk Polypharmacy (Cluster 0)     │
     │ 8 patients  |  Avg meds: 12.3  |  78% DDI │
     └───────────────────────────────────────────┘
     ```

**2. Create `/api/clusters` endpoint**:
```python
@app.get("/api/clusters")
async def get_clusters():
    df = parquet_reader.get_patient_features()
    clusters = df.groupby('Cluster').agg({
        'PatientSID': 'count',
        'MedicationCount': 'mean',
        'DDIPairCount': 'mean'
    })
    return clusters.to_dict('records')
```

**3. Add simple bar chart for cluster distribution (Plotly)**

**Deliverable**: Real data displayed on homepage

---

### **Phase 3: Patient Features (Week 3)**

**Goal**: Patient list and detail views

#### **Tasks**:

**1. Create `/patients` route → patient list table**:
   - Columns: PatientSID, Age, Gender, Cluster, Med Count, DDI Count
   - HTMX search/filter
   - Click row → patient detail

**2. Create `/patients/{patient_id}` route → patient detail**:
   - Demographics card
   - Medication timeline (Gantt-style with Plotly)
   - DDI alerts table
   - Cluster membership badge

**3. Add HTMX filtering**:
```html
<input
    type="search"
    name="q"
    hx-get="/patients/search"
    hx-target="#patient-table"
    hx-trigger="keyup changed delay:500ms"
>
```

**Deliverable**: Navigate from patient list → patient detail

---

### **Phase 4: DDI Explorer (Week 3-4)**

**Goal**: DDI pair exploration and "Blind Spot" detection

#### **Tasks**:

**1. Create `/ddi` route → DDI pair explorer**:
   - Table of 71 DDI pairs
   - Filter by severity, drug name
   - Show affected patients

**2. Create `/blind-spot` route → concurrent care analysis**:
   - Show 10 patients with dual-source meds
   - Highlight DDIs spanning VA + Community
   - Timeline showing overlap period

**3. Add severity color coding**:
```css
.severity-high { background: #fee2e2; color: #b91c1c; }
.severity-moderate { background: #fef9c3; color: #a16207; }
```

**Deliverable**: DDI exploration and unique "Blind Spot" feature

---

### **Phase 5: Polish & Advanced (Week 4+)**

**Goal**: Charts, high-risk alerts, export

#### **Tasks**:

**1. Add Plotly visualizations**:
   - Cluster scatter plot (age vs med count, colored by cluster)
   - DDI distribution histogram
   - Medication timeline (Gantt chart)

**2. Create `/alerts` route**:
   - Top 10 high-risk patients
   - Recent DDI detections
   - Data quality issues

**3. Add export functionality**:
   - "Download Report" button → PDF or CSV
   - Export patient list
   - Export DDI pairs

**4. Styling improvements**:
   - Dark mode toggle
   - Print-friendly CSS
   - Loading states for HTMX

**Deliverable**: Production-ready dashboard

---

## Part 5: Specific Recommendations

### **Critical Path Items**

1. **START HERE**: Create `requirements.txt`, `.env`, `config.py` (1 day)
2. **NEXT**: Build `data/parquet_reader.py` and test loading med-ml files (1 day)
3. **THEN**: Replace homepage with real cluster data (2 days)
4. **AFTER**: Build patient list/detail (3 days)
5. **FINALLY**: DDI explorer and Blind Spot (3 days)

### **Quick Wins** (High Impact, Low Effort)

1. **Replace index.html metrics** with real counts from Parquet files
2. **Add cluster tiles** using med-ml clustering output
3. **Build patient list table** with search (HTMX demo is already working)
4. **Color-code risk levels** using existing status pill CSS

### **Unique Differentiators**

These features will make your dashboard stand out:

1. **"Blind Spot" Detection**: Show concurrent VA + Community DDIs (unique to your project)
2. **Cluster-based interventions**: Show cluster-specific recommendations
3. **Temporal visualization**: Medication timeline showing dual-source overlap
4. **Interactive exploration**: HTMX-powered filtering without page reloads

---

## Part 6: Code Quality Suggestions

### **Current Code Issues to Address**

1. **main.py line 38-48**: Move hardcoded data to database/Parquet
2. **base.html line 48-59**: Implement missing routes (Datasets, Alerts, Settings)
3. **No error handling**: Add try/except for data loading failures
4. **No logging**: Add logging for debugging
5. **Timer/HTMX demos**: Consider removing or repurposing for domain use

### **Best Practices to Add**

1. **Dependency injection**: Pass data readers to routes
2. **Response models**: Use Pydantic for API validation
3. **Caching**: Cache Parquet reads (they're slow)
4. **Security**: Add CORS, CSP headers
5. **Testing**: Add pytest for route testing

---

## Part 7: Estimated Timeline

**Conservative estimate** (solo developer, part-time):

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Phase 1** | 3-4 days | Data connections working |
| **Phase 2** | 4-5 days | Real dashboard homepage |
| **Phase 3** | 5-6 days | Patient list + detail views |
| **Phase 4** | 4-5 days | DDI explorer + Blind Spot |
| **Phase 5** | 5-7 days | Charts, alerts, polish |
| **TOTAL** | **3-4 weeks** | Production-ready DDI dashboard |

**Aggressive estimate** (full-time, focused work): **2 weeks**

---

## Part 8: Final Assessment

### **Current Maturity Level**: ⭐⭐ / 5

- ✅ **Architecture**: 4/5 (solid foundation)
- ⚠️ **Functionality**: 1/5 (demos only)
- ⚠️ **Domain Fit**: 1/5 (not healthcare-specific yet)
- ✅ **Code Quality**: 4/5 (clean, well-structured)
- ⚠️ **Data Integration**: 0/5 (none)

### **Target Maturity Level**: ⭐⭐⭐⭐ / 5

After implementing the roadmap, you'll have:
- ✅ Full-stack DDI risk dashboard
- ✅ Real data from med-ml + med-data
- ✅ Unique "Blind Spot" concurrent care feature
- ✅ Interactive exploration with HTMX
- ✅ Portfolio-ready demonstration

---

## Part 9: Next Steps

### **Recommended Approach**:

1. **Review this assessment** and ask any clarifying questions
2. **Confirm priorities**: Which features matter most to you?
3. **Choose starting point**: Phase 1 (data connections) is critical path
4. **Iterative development**: Build feature-by-feature, test early

### **Questions to Consider**:

1. Do you want to start with Phase 1 (infrastructure)?
2. Are there any features you want to prioritize or skip?
3. Would you prefer a different visualization library (Chart.js instead of Plotly)?
4. Do you want to keep the Timer/HTMX demo pages or remove them?
5. Should we add authentication/user management?

---

## Appendix A: Key File Locations from med-ml

### **Parquet Files to Read** (in MinIO `med-data` bucket):

```
v3_features/ddi/
├── patients_features_clustered.parquet    # Patient-level features + cluster assignments
├── ddi_pairs_features.parquet             # DDI pair-level features
└── patient_ddi_pairs.parquet              # Patient-DDI relationships

v1_raw/medications/
└── medications_combined.parquet           # All medications (VA + Community)

v1_raw/ddi/
└── ddi_reference.parquet                  # DDI reference data (severity, descriptions)
```

### **SQL Server Tables** (in CDWWork database):

```
SPatient.SPatient                          # Patient demographics (Age, Gender, DOB)
Dim.Sta3n                                  # Facility information
```

---

## Appendix B: Sample Data Schemas

### **patients_features_clustered.parquet**:
```python
{
    'PatientSID': int,
    'Age': int,
    'Gender': str,
    'Cluster': int,                        # 0, 1, or 2
    'MedicationCount': int,
    'UniqueDrugsCount': int,
    'DDIPairCount': int,
    'HighSeverityDDICount': int,
    'HasConcurrentCare': bool,             # True if MIMIC-Community meds
    # ... 19 total features
}
```

### **ddi_pairs_features.parquet**:
```python
{
    'Drug1': str,
    'Drug2': str,
    'Severity': str,                       # 'high', 'moderate', 'low'
    'InteractionType': str,
    'Description': str,
    'PatientCount': int,                   # How many patients affected
    'CrossSourceDDI': bool                 # True if spans VA + Community
}
```

---

**End of Assessment**
