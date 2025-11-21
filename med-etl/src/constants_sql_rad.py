# constants_sql_rad.py
"""Constants for SLQ statements"""

RAD_EXTRACT_NAME = "RAD"
RAD_EXTRACT_VERSION = "1.0"
RAD_PARQUET_FILENAME = "rad_sample_20250603.parquet"

# insert finalized records ito Extract database
RAD_INSERT_01 = """
    --
    -- Insert each finalized record into Extract.Data.RAD table
    --
    INSERT INTO [Data].RAD (
        DivisionIEN, PatientIEN, PatientSSN, LName4, InOutPatient, PatXferDate, CPTCodeMod, RadProcedure,
        RadLocationIEN, LocationIEN, ServiceSectionIEN, SpecialtyIEN, Placeholder22, Placeholder23, Placeholder24,
        StopCode, CreditMethod, PlaceholderCerner, CaseNumber, PlaceholderNewMPI, PlaceholderSIGI, RunStartDate,
        RunEndDate, RunSta3n, ExtractName, ExtractVersion, ExtractStatus, QueryTimestamp, QueryUser
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?
    )
"""
