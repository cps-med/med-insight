/*
|---------------------------------------------------------------
| Create: Data.RAD.sql
|---------------------------------------------------------------
*/

-- set the active database
USE Extract;
GO

-- create RAD table in the Data schema
CREATE TABLE [Data].RAD (
    DivisionIEN                SMALLINT         NOT NULL,
    PatientIEN                 VARCHAR(50)      NOT NULL,
    PatientSSN                 VARCHAR(20)      NULL,
    LName4                     VARCHAR(4)       NOT NULL,
    InOutPatient               CHAR(1)          NOT NULL,
    PatXferDate                DATE             NOT NULL,
    CPTCodeMod                 VARCHAR(7)       NULL,
    RadProcedure               VARCHAR(50)      NULL,
    RadLocationIEN             VARCHAR(50)      NULL,
    LocationIEN                VARCHAR(50)      NULL,
    ServiceSectionIEN          VARCHAR(50)      NULL,
    SpecialtyIEN               VARCHAR(50)      NULL,
    Placeholder22              CHAR(1)          NOT NULL,
    Placeholder23              CHAR(1)          NOT NULL,
    Placeholder24              CHAR(1)          NOT NULL,
    StopCode                   VARCHAR(10)      NULL,
    CreditMethod               CHAR(1)          NULL,
    PlaceholderCerner          CHAR(1)          NOT NULL,
    CaseNumber                 VARCHAR(5)       NULL,
    PlaceholderNewMPI          CHAR(1)          NOT NULL,
    PlaceholderSIGI            CHAR(1)          NOT NULL,
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

-- create indexes for the Data.ADM table
CREATE INDEX IX_PatientIEN ON Data.RAD (PatientIEN);
CREATE INDEX IX_PatientSSN ON Data.RAD (PatientSSN);
CREATE INDEX IX_RunSta3n ON Data.RAD (RunSta3n);
CREATE INDEX IX_ExtractName ON Data.RAD (ExtractName);
CREATE INDEX IX_QueryTimestamp ON Data.RAD (QueryTimestamp);
GO
