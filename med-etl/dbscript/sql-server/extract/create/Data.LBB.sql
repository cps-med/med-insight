/*
|---------------------------------------------------------------
| Create: Data.LBB.sql
|---------------------------------------------------------------
*/

-- set the active database
USE Extract;
GO

-- create LBB table in the Data schema
CREATE TABLE [Data].LBB (
    DivisionIEN                SMALLINT         NOT NULL,
    PatientIEN                 VARCHAR(50)      NOT NULL,
    PatientSSN                 VARCHAR(20)      NULL,
    LName4                     VARCHAR(4)       NOT NULL,
    InOutPatient               CHAR(1)          NOT NULL,
    EncounterNumber            VARCHAR(50)      NOT NULL,
    TransfusionDate            DATE             NOT NULL,
    TransfusionTime            TIME             NOT NULL,
    Component                  VARCHAR(50)      NOT NULL,
    ComponentAbbr              VARCHAR(10)      NOT NULL,
    NumberUnits                SMALLINT         NOT NULL,
    Volume                     SMALLINT         NOT NULL,
    Reaction                   CHAR(1)          NOT NULL,
    ReactionType               INT              NOT NULL,
    FeederLocation             VARCHAR(30)      NOT NULL,
    Placeholder16              CHAR(1)          NULL,
    Placeholder17              CHAR(1)          NULL,
    OrderingProvider           INT              NOT NULL,
    OrderingProviderPC         INT              NOT NULL,
    ERI                        CHAR(1)          NULL,
    UnitModified               CHAR(1)          NOT NULL,
    UnitModification           VARCHAR(30)      NULL,
    RequestingProv             INT              NOT NULL,
    RequestingProviderPC       INT              NOT NULL,
    ProdDivisionCode           INT              NULL,
    OrderingProviderNPI        INT              NULL,
    RequestingProviderNPI      INT              NULL,
    Placeholder28              CHAR(1)          NULL,
    Placeholder29              CHAR(1)          NULL,
    Placeholder30              CHAR(1)          NULL,
    Placeholder31              CHAR(1)          NULL,
    Placeholder32              CHAR(1)          NULL,
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
CREATE INDEX IX_PatientIEN ON Data.LBB (PatientIEN);
CREATE INDEX IX_PatientSSN ON Data.LBB (PatientSSN);
CREATE INDEX IX_RunSta3n ON Data.LBB (RunSta3n);
CREATE INDEX IX_ExtractName ON Data.LBB (ExtractName);
CREATE INDEX IX_QueryTimestamp ON Data.LBB (QueryTimestamp);
GO
