"""
csv_to_parquet.py

Convert various CSV files to equivelent Parquet format
"""

import pandas as pd

# -----------------------------------------------------------------------------
# SPatient/Spatient: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV file into DataFrame
# df = pd.read_csv('~/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/spatient/spatient/spatient_mock_20250807.csv')

# ensure proper typing for some of the fields
# df["PatientIEN"] = df["PatientIEN"].astype(str)
# df["ScrSSN"] = df["ScrSSN"].astype(str)
# df["PatientSSN"] = df["PatientSSN"].astype(str)

# write to Parquet
# df.to_parquet('~/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/spatient/spatient/spatient_mock_20250807.parquet')

# -----------------------------------------------------------------------------
# SStaff/Staff: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV file into DataFrame
# df = pd.read_csv('~/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/sstaff/sstaff/sstaff_mock_20250807.csv')

# ensure proper typing for some of the fields
# df["StaffIEN"] = df["StaffIEN"].astype(str)
# df["StaffSSN"] = df["StaffSSN"].astype(str)

# write to Parquet
# df.to_parquet('~/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/sstaff/sstaff/sstaff_mock_20250807.parquet')

# -----------------------------------------------------------------------------
# visitdatetime_quarter=20251: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV file into DataFrame
# df = pd.read_csv('~/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/outpat/visit/visitdatetime_year=2025/visitdatetime_quarter=20251/visitdatetime_quarter=20251_v2.csv')

# ensure consistent typing for key columns
# df["VisitDateTime"] = df["VisitDateTime"].astype(str)
# df["EncounterDateTime"] = df["EncounterDateTime"].astype(str)

# write to Parquet
# df.to_parquet('/Users/chuck/swdev/med/med-insight/med-data/adls-gen2/ci-published/vista/current/outpat/visit/visitdatetime_year=2025/visitdatetime_quarter=20251/visitdatetime_quarter=20251_v2.parquet')

# -----------------------------------------------------------------------------
# LBB: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV
# df = pd.read_csv('~/swdev/med/med-insight/med-data/adls-gen2/med-sandbox/extract-file/lbb/lbb_sample_20250731.csv')

# ensure proper typing for some of fields
# df["patient_ssn"] = df["patient_ssn"].astype(str)

# write to Parquet
# df.to_parquet('~/swdev/med/med-insight/med-data/adls-gen2/med-sandbox/extract-file/lbb/lbb_sample_20250731.parquet')


# -----------------------------------------------------------------------------
# LBB: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV
#df = pd.read_csv('~/swdev/med/med-data/adls-gen2/med-sandbox/extract-file/rad/rad_sample_20250603.csv')

# write to Parquet
#df.to_parquet('~/swdev/med/med-data/adls-gen2/med-sandbox/extract-file/rad/rad_sample_20250603.parquet')


# -----------------------------------------------------------------------------
# CLI: read CSV file and write to Parquet file
# -----------------------------------------------------------------------------
# read CSV
df = pd.read_csv('~/swdev/med/med-data/adls-gen2/med-sandbox/extract-file/cli/cli_sample_20251113.csv')

# write to Parquet
df.to_parquet('~/swdev/med/med-data/adls-gen2/med-sandbox/extract-file/cli/cli_sample_20251113.parquet')


# -----------------------------------------------------------------------------
# More entailed code code to format and write visitdatetime_quarter=2025 file
# -----------------------------------------------------------------------------
# ensure consistent typing for key columns
#df["visitdatetime_year"] = df["visitdatetime_year"].astype(str)
#df["visitdatetime_quarter"] = df["visitdatetime_quarter"].astype(str)

# write to Parquet
#df.to_parquet('/Users/chuck/swdev/med/med-data/adls-gen2/vista-data/current/outpat/visit/visitdatetime_year=2025/visitdatetime_quarter=20251/visitdatetime_quarter=20251.parquet')
