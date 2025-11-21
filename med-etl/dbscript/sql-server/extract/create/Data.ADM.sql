/*
|---------------------------------------------------------------
| Create: Data.ADM.sql
|---------------------------------------------------------------
*/

-- set the active database
USE Extract;
GO

-- create ADM table in the Data schema
CREATE TABLE [Data].ADM (
    DivisionIEN                SMALLINT         NOT NULL,
    PatientIEN                 VARCHAR(50)      NOT NULL,
    PatientSSN                 VARCHAR(20)      NULL,
    LName4                     VARCHAR(4)       NOT NULL,
    InOutPatient               CHAR(1)          NOT NULL,
    PatXferDate                DATE             NOT NULL,
    PrimaryCareTeam            VARCHAR(50)      NULL,
    Gender                     CHAR(1)          NOT NULL,
    PatientBirthDate           DATE             NOT NULL,
    Religion                   VARCHAR(20)      NULL,
    AddressEmpStatus           CHAR(1)          NOT NULL,
    HealthInsurance            CHAR(1)          NOT NULL,
    VAStateCode                VARCHAR(10)      NOT NULL,
    County                     VARCHAR(50)      NOT NULL,
    Zip4                       VARCHAR(50)      NULL,
    EligibilityVACode          VARCHAR(30)      NULL,
    VeteranFlag                CHAR(1)          NULL,
    Vietnam                    CHAR(1)          NULL,
    AgentOrangeExposureCode    VARCHAR(50)      NULL,
    IonizingRadiationCode      VARCHAR(50)      NULL,
    POWStatusCode              VARCHAR(50)      NULL,
    PeriodOfServiceCode        VARCHAR(50)      NULL,
    MeansTest                  VARCHAR(10)      NULL,
    MaritalStatus              CHAR(1)          NOT NULL,
    WardLocationIEN            VARCHAR(50)      NOT NULL,
    TreatingSpecialty          VARCHAR(50)      NULL,
    StaffIEN                   VARCHAR(50)      NULL,
    MovementFileNum            VARCHAR(20)      NULL,
    PlaceholderDRG             CHAR(1)          NOT NULL,
    Placeholder30              CHAR(1)          NOT NULL,
    PatXferTime                CHAR(6)          NOT NULL,
    PlaceholderPcProvider      VARCHAR(50)      NULL,
    PlaceholderRace            VARCHAR(50)      NULL,
    PrimaryWardProvider        VARCHAR(50)      NULL,
    MPI                        VARCHAR(20)      NULL,
    Placeholder36              CHAR(1)          NOT NULL,
    Placeholder37              CHAR(1)          NOT NULL,
    Placeholder38              CHAR(1)          NOT NULL,
    Placeholder39              CHAR(1)          NOT NULL,
    AdmissionEligibility       VARCHAR(10)      NULL,
    MSTStatus                  CHAR(1)          NULL,
    SHADFlag                   CHAR(1)          NULL,
    Placeholder43              CHAR(1)          NOT NULL,
    Placeholder44              CHAR(1)          NOT NULL,
    EnrollmentLocation         SMALLINT         NOT NULL,
    Placeholder46              CHAR(1)          NOT NULL,
    Placeholder47              CHAR(1)          NOT NULL,
    Placeholder48              CHAR(1)          NOT NULL,
    Placeholder49              CHAR(1)          NOT NULL,
    Dom                        CHAR(1)          NULL,
    EnrollmentCategory         CHAR(1)          NULL,
    EnrollmentStatus           CHAR(2)          NULL,
    EncounterSHAD              CHAR(1)          NULL,
    PurpleHeart                CHAR(1)          NULL,
    ObservationPt              CHAR(1)          NULL,
    AgentOrangeLocation        VARCHAR(50)      NULL,
    POWLocation                VARCHAR(50)      NULL,
    Placeholder62              CHAR(1)          NOT NULL,
    Placeholder63              CHAR(1)          NOT NULL,
    Placeholder70              CHAR(1)          NOT NULL,
    SWAsiaCode                 VARCHAR(50)      NULL,
    Placeholder82              CHAR(1)          NOT NULL,
    NPI                        VARCHAR(50)      NULL,
    Placeholder84              CHAR(1)          NOT NULL,
    CountryCode                VARCHAR(50)      NULL,
    EligibilityStatus          VARCHAR(30)      NULL,
    CampLejeuneFlag            CHAR(1)          NULL,
    PlaceholderCerner          CHAR(1)          NOT NULL,
    PatientICN                 VARCHAR(50)      NULL,
    SIGI                       VARCHAR(20)      NULL,
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
CREATE INDEX IX_PatientIEN ON Data.ADM (PatientIEN);
CREATE INDEX IX_PatientSSN ON Data.ADM (PatientSSN);
CREATE INDEX IX_EnrollmentLocation ON Data.ADM (EnrollmentLocation);
CREATE INDEX IX_RunSta3n ON Data.ADM (RunSta3n);
CREATE INDEX IX_ExtractName ON Data.ADM (ExtractName);
CREATE INDEX IX_QueryTimestamp ON Data.ADM (QueryTimestamp);
GO
