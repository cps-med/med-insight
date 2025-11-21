/*
|---------------------------------------------------------------
| Create: Data.CLI.sql
|---------------------------------------------------------------
*/

-- set the active database
USE Extract;
GO

-- create CLI table in the Data schema
CREATE TABLE [Data].CLI (
    Facility                   SMALLINT         NOT NULL,
    PatientNumDFN              VARCHAR(20)      NOT NULL,
    PatientSSN                 VARCHAR(20)      NULL,
    LName4                     VARCHAR(4)       NOT NULL,
    InOutPatientInd            CHAR(1)          NOT NULL,
    VisitDate                  DATE             NOT NULL,
    PH007                      CHAR(1)          NOT NULL,
    OverbookedIndicator        CHAR(1)          NOT NULL,
    PH009                      CHAR(1)          NOT NULL,
    TreatingSpecialty          VARCHAR(8)       NOT NULL,
    VisitTime                  TIME             NOT NULL,
    PH012                      CHAR(1)          NOT NULL,
    PH013                      CHAR(1)          NOT NULL,
    PH014                      CHAR(1)          NOT NULL,
    WorkloadProvider           VARCHAR(20)      NOT NULL,
    ProviderPersonClass        VARCHAR(20)      NOT NULL,
    PH017                      CHAR(1)          NOT NULL,
    PH018                      CHAR(1)          NOT NULL,
    PH019                      CHAR(1)          NOT NULL,
    PH020                      CHAR(1)          NOT NULL,
    PH021                      CHAR(1)          NOT NULL,
    PH022                      CHAR(1)          NOT NULL,
    PH023                      CHAR(1)          NOT NULL,
    PH024                      CHAR(1)          NOT NULL,
    PH025                      CHAR(1)          NOT NULL,
    PH026                      CHAR(1)          NOT NULL,
    PH027                      CHAR(1)          NOT NULL,
    PH028                      CHAR(1)          NOT NULL,
    PH029                      CHAR(1)          NOT NULL,
    PH030                      CHAR(1)          NOT NULL,
    PH031                      CHAR(1)          NOT NULL,
    PH032                      CHAR(1)          NOT NULL,
    PH033                      CHAR(1)          NOT NULL,
    PH034                      CHAR(1)          NOT NULL,
    PH035                      CHAR(1)          NOT NULL,
    PH036                      CHAR(1)          NOT NULL,
    RadiationEncIndicator      CHAR(1)          NOT NULL,
    PH038                      CHAR(1)          NOT NULL,
    AgentOrangeEncIndicator    CHAR(1)          NOT NULL,
    PH040                      CHAR(1)          NOT NULL,
    PH041                      CHAR(1)          NOT NULL,
    PH042                      CHAR(1)          NOT NULL,
    PH043                      CHAR(1)          NOT NULL,
    PH044                      CHAR(1)          NOT NULL,
    PH045                      CHAR(1)          NOT NULL,
    EncounterEligibility       VARCHAR(4)       NULL,
    PH047                      CHAR(1)          NOT NULL,
    MstEncounterInd            CHAR(1)          NULL,
    PH049                      CHAR(1)          NOT NULL,
    PH050                      CHAR(1)          NOT NULL,
    PH051                      CHAR(1)          NOT NULL,
    PH052                      CHAR(1)          NOT NULL,
    PH053                      CHAR(1)          NOT NULL,
    PH054                      CHAR(1)          NOT NULL,
    PH055                      CHAR(1)          NOT NULL,
    PH056                      CHAR(1)          NOT NULL,
    DomPrrtpSaartp             CHAR(1)          NULL,

    -- Metadata columns
    RunStartDate               DATE             NOT NULL,
    RunEndDate                 DATE             NOT NULL,
    RunSta3n                   SMALLINT         NOT NULL,
    ExtractName                VARCHAR(3)       NOT NULL,
    ExtractVersion             VARCHAR(20)      NOT NULL,
    ExtractStatus              VARCHAR(20)      NOT NULL,
    QueryTimestamp             DATETIME2        NOT NULL,
    QueryUser                  NVARCHAR(128)    NULL
);
GO

-- create indexes for the Data.CLI table
CREATE INDEX IX_FacilityIEN ON Data.CLI (FacilityIEN);
CREATE INDEX IX_PatientNumDFN ON Data.CLI (PatientIEN);
CREATE INDEX IX_PatientSSN ON Data.CLI (PatientSSN);
CREATE INDEX IX_RunSta3n ON Data.CLI (RunSta3n);
CREATE INDEX IX_ExtractName ON Data.CLI (ExtractName);
CREATE INDEX IX_QueryTimestamp ON Data.CLI (QueryTimestamp);
GO
