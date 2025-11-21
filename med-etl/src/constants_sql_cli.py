# constants_sql_lbb.py
"""Constants for SLQ statements"""

CLI_EXTRACT_NAME = "CLI"
CLI_EXTRACT_VERSION = "1.0"
CLI_PARQUET_FILENAME = "cli_sample_20251113.parquet"

# insert finalized records ito Extract database
CLI_INSERT_01 = """
    --
    -- Insert each finalized record into Extract.Data.LBB table
    --
    INSERT INTO [Data].CLI (
        DivisionIEN, PatientIEN, PatientSSN, LName4, InOutPatient, EncounterNumber, TransfusionDate, TransfusionTime,
        Component, ComponentAbbr, NumberUnits, Volume, Reaction, ReactionType, FeederLocation, Placeholder16,
        Placeholder17, OrderingProvider, OrderingProviderPC, ERI, UnitModified, UnitModification, RequestingProv,
        RequestingProviderPC, ProdDivisionCode, OrderingProviderNPI, RequestingProviderNPI, Placeholder28, Placeholder29,
        Placeholder30, Placeholder31, Placeholder32, RunStartDate, RunEndDate, RunSta3n, ExtractName, ExtractVersion,
        ExtractStatus, QueryTimestamp, QueryUser
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?
    )
"""
