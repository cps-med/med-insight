# -----------------------------------------------------------------------
# constants_sql_adm.py
# -----------------------------------------------------------------------
# Constants for ADM SQL statements
#  - ADM_QUERY_00, ADM_QUERY_01, ADM_QUERY_02
#  - ADM_QUERY_03, ADM_QUERY_04, ADM_QUERY_05
#  - ADM_INSERT_01
# -----------------------------------------------------------------------

ADM_EXTRACT_NAME = "ADM"
ADM_EXTRACT_VERSION = "1.0"

# Full query to get all data from all tables and performs all steps
# (use for manual testing - try to keep this up-to-date)
# (this query is likely out of date and inconsisent with the scripts below)
ADM_QUERY_00 = """
    --
    -- This query is based on the CDW Inpat.PatientTransfer table
    -- Make sure you have selected CDWWork as the active database
    -- Before running, replace the three ? placeholder values in the WHERE clause
    -- For example: 508, '2025-01-01', and '2025-01-05'
    --

    SELECT  d.DivisionIEN,
            p.PatientIEN,
            p.PatientSSN,       
            LEFT(p.PatientLastName, 4) AS LName4,
            'I' AS InOutPatient,
            REPLACE(CONVERT(VARCHAR(10), pt.PatientTransferDateTime, 120), '-', '') AS PatXferDate,
            '' AS PrimaryCareTeam,
            p.Gender,
            REPLACE(CONVERT(VARCHAR(10), p.BirthDateTime, 120), '-', '') AS PatientBirthDate,
            '' AS Religion,

            -- Get and map Employment Status from Patient Address table
            CASE
                WHEN pa.EmploymentStatus = 'EMPLOYED FULL TIME' THEN '1'
                WHEN pa.EmploymentStatus = 'EMPLOYED PART TIME' THEN '2'
                WHEN pa.EmploymentStatus = 'NOT EMPLOYED' THEN '3'
                WHEN pa.EmploymentStatus = 'SELF EMPLOYED' THEN '4'
                WHEN pa.EmploymentStatus = 'RETIRED' THEN '5'
                WHEN pa.EmploymentStatus = 'ACTIVE MILITARY DUTY' THEN '6'
                ELSE '9'
            END AS AddressEmpStatus,

            '1' AS HealthInsurance,
            s2.VAStateCode,
            pa.County,   -- should this be a numeric coded value?
            pa.Zip4,
            p.EligibilityVACode,
            p.VeteranFlag,
            'N' AS Vietnam,
            pd.AgentOrangeExposureCode,
            pd.IonizingRadiationCode,
            pd.POWStatusCode,
            pos.PeriodOfServiceCode,
            '' AS MeansTest,

            -- Get and map Patient Marital Status
            CASE
                WHEN p.MaritalStatus = 'DIVORCED' THEN '1'
                WHEN p.MaritalStatus = 'MARRIED' THEN '2'
                WHEN p.MaritalStatus = 'WIDOWED' THEN '4'
                WHEN p.MaritalStatus = 'SEPARATED' THEN '5'
                WHEN p.MaritalStatus = 'NEVER MARRIED' THEN '6'
                WHEN p.MaritalStatus = 'UNKNOWN' THEN '7'
                ELSE ''
            END AS MaritalStatus,

            wl.WardLocationIEN,
            'TreatSpec' AS TreatingSpecialty,
            s.StaffIEN,
            '12345678' AS MovementFileNum,
            '' AS PlaceholderDRG,
            '' AS Placeholder30,

            -- Get the time component of the PT DateTime field
            REPLACE(CONVERT(VARCHAR(8), pt.PatientTransferDateTime, 108), ':', '') AS PatXferTime,

            '' AS PlaceholderPcProvider,
            '' AS PlaceholderRace,
            'PriWardProv' AS PrimaryWardProvider,
            '' AS MPI,
            '' AS Placeholder36,
            '' AS Placeholder37,
            '' AS Placeholder38,
            '' AS Placeholder39,
            '10' AS AdmissionEligibility,
            'U' AS MSTStatus,
            pd.SHADFlag,
            '' AS Placeholder43,
            '' AS Placeholder44,

            -- Using p.Sta3n for now (determine if enrollment file needed)
            p.Sta3n AS EnrollmentLocation,

            '' AS Placeholder46,
            '' AS Placeholder47,
            '' AS Placeholder48,
            '' AS Placeholder49,
            'D' AS Dom,
            '?' AS EnrollmentCategory,
            '??' AS EnrollmentStatus,
            'N' AS EncounterSHAD,
            'N' AS PurpleHeart,
            'N' AS ObservationPt,

            -- Add "Encounter Number"

            pd.AgentOrangeLocation,

            -- Add "Production Division Code"

            pd.POWLocation,

            '' AS Placeholder62,
            '' AS Placeholder63,
            
            -- skipping down a bit...
            '' AS Placeholder70,
            pd.SWAsiaCode,
            pd.AgentOrangeExposureCode,  -- is this a duplicate?
            '' AS Placeholder82,
            s.NPI,
            '' AS Placeholder84,
            s.NPI,
            c.CountryCode,
            p.EligibilityStatus,

            pd.CampLejeuneFlag,

            -- skipping down a bit...
            '' AS PlaceholderCerner,
            p.PatientICN,
            p.SelfIdentifiedGender

    FROM Inpat.PatientTransfer AS pt

    INNER JOIN SPatient.SPatient AS p ON pt.PatientSID = p.PatientSID
    INNER JOIN SPatient.SPatientAddress AS pa ON pt.PatientSID = pa.PatientSID
    INNER JOIN Dim.State AS s2 ON s2.StateSID = pa.StateSID
    INNER JOIN Dim.Country AS c ON pa.CountrySID = c.CountrySID    
    INNER JOIN Spatient.SpatientDisability AS pd ON pt.PatientSID = pd.PatientSID
    INNER JOIN Dim.WardLocation AS wl ON pt.GainingWardLocationSID = wl.WardLocationSID
    INNER JOIN Dim.Division AS d ON wl.DivisionSID = d.DivisionSID
    INNER JOIN Dim.PeriodOfService AS pos ON p.PeriodOfServiceSID = pos.PeriodOfServiceSID
    INNER JOIN SStaff.SStaff AS s ON pt.AttendingPhysicianStaffSID = s.StaffSID
    INNER JOIN Dim.VistASite AS v ON pt.Sta3n = Dim.VistASite.Sta3n

    WHERE
        -- Get latest Patient Address record per Ordinal Number via subquery
        pa.OrdinalNumber = (
            SELECT MAX(pa2.OrdinalNumber)
            FROM SPatient.SPatientAddress AS pa2
            WHERE pa2.PatientSID = pt.PatientSID 
        )
        and pt.Sta3n = ?
        and pt.PatientTransferDateTime >= ?
        and pt.PatientTransferDateTime < ?
        
    ORDER BY pt.PatientTransferDateTime;
"""

# Initial query to get record set that meets criterial for patient movement
# Run and save to a global temporary table
ADM_QUERY_01 = """
    --
    -- Get base record set from Inpat.PatientTransfer and write results to a temporary table
    -- 
    -- The correct way to do this is to use Inpat.ProvisionalMovement as the base table and then
    -- LEFT OUTER JOIN with Inpat.PatientTransfer, Inpat.SpecialtyTransfer, Inpat.Inpatient,
    -- Inpat.SpecialtyTransfer, and Outpat.Visit.
    -- 
    -- Before running, replace the ? placeholder values in the WHERE clause
    -- For example: 508, '2025-01-01', and '2025-01-03'
    --
    SELECT
        pt.PatientSID,
        pt.PatientTransferDateTime,
        pt.GainingWardLocationSID,
        pt.Sta3n,
        pt.AttendingPhysicianStaffSID,
        pt.InpatientSID
    INTO ##AdmPatientCohort
    FROM Inpat.PatientTransfer AS pt
    WHERE pt.Sta3n = ?
        AND pt.PatientTransferDateTime >= ?
        AND pt.PatientTransferDateTime < ?;
"""

# check results from prior query
ADM_QUERY_02 = """
    --
    -- Check results from prior query
    --
    SELECT *
    FROM ##AdmPatientCohort;
"""

# perform joins to produce full record
ADM_QUERY_03 = """
    --
    -- Join ##AdmPatientCohort with additional tables to get all ADM data elements
    -- Store result into an additional temporary table
    --
    SELECT
        ---- SPatient.SPatient data as p ----
        p.PatientIEN, 
        p.PatientSSN,    
        p.PatientLastName, 
        p.Gender, 
        p.BirthDateTime,
        p.EligibilityVACode,
        p.VeteranFlag,
        p.MaritalStatus,
        p.Sta3n AS EnrollmentLocation,
        p.PatientICN,
        p.SelfIdentifiedGender AS SIGI,
        p.EligibilityStatus,
        ---- SPatient.SpatientAddress as pa ----
        pa.EmploymentStatus,
        pa.County,
        pa.Zip4,
        ---- Dim.State as s2 ----
        s2.VAStateCode,
        ---- Dim.Country as c ----
        c.CountryCode,
        ---- Spatient.SpatientDisability as pd ----
        pd.AgentOrangeLocation,
        pd.AgentOrangeExposureCode,
        pd.POWLocation,
        pd.IonizingRadiationCode,
        pd.POWStatusCode,
        pd.SHADFlag,
        pd.SWAsiaCode,
        pd.CampLejeuneFlag,
        ---- Dim.WardLocation as wl ----
        wl.WardLocationIEN,
        ---- Dim.Division as d ----
        d.DivisionIEN,
        ---- Dim.PeriodOfService as pos ----
        pos.PeriodOfServiceCode,
        ---- SStaff.SStaff as s ----
        s.StaffIEN,
        s.NPI,
        ---- Inpatient.Inpatient as i ----
        i.AdmitWardLocationSID,
        ---- Dim.VistASite as v ---- (bonus field, not part of extract)
        v.Sta3n,
        ---- p.PatientName ---- (bonus field, not part of extract)
        p.PatientName,
        ---- apc.PatientTransferDateTime
        apc.PatientTransferDateTime

    INTO ##AdmPatientExtract
    FROM ##AdmPatientCohort AS apc

    INNER JOIN SPatient.SPatient AS p             ON  apc.PatientSID = p.PatientSID
    INNER JOIN SPatient.SPatientAddress AS pa     ON  apc.PatientSID = pa.PatientSID
    INNER JOIN Dim.State AS s2                    ON  s2.StateSID = pa.StateSID
    INNER JOIN Dim.Country AS c                   ON  pa.CountrySID = c.CountrySID    
    INNER JOIN Spatient.SpatientDisability AS pd  ON  apc.PatientSID = pd.PatientSID
    INNER JOIN Dim.WardLocation AS wl             ON  apc.GainingWardLocationSID = wl.WardLocationSID
    INNER JOIN Dim.Division AS d                  ON  wl.DivisionSID = d.DivisionSID
    INNER JOIN Dim.PeriodOfService AS pos         ON  p.PeriodOfServiceSID = pos.PeriodOfServiceSID
    INNER JOIN SStaff.SStaff AS s                 ON  apc.AttendingPhysicianStaffSID = s.StaffSID
    INNER JOIN Inpat.Inpatient AS i               ON  apc.PatientSID = i.PatientSID
    INNER JOIN Dim.VistASite AS v                 ON  apc.Sta3n = v.Sta3n

    WHERE
        -- Get latest Patient Address record per Ordinal Number via subquery
        pa.OrdinalNumber = (
            SELECT MAX(pa2.OrdinalNumber)
            FROM SPatient.SPatientAddress AS pa2
            WHERE pa2.PatientSID = apc.PatientSID
        );
"""

# check results from prior query
ADM_QUERY_04 = """
    --
    -- Check results from prior query (unsorted)
    --
    SELECT *
    FROM ##AdmPatientExtract;
"""

# create final form records (transform and sort)
# this is also an opportunity to update the column names for insertion into Extract.Data.ADM table
# for example, DivisionIEN as Facility
ADM_QUERY_05 = """
    --
    -- Create final extract format (transform and sort)
    -- Also add placeholder and hardcoded fields
    --
    SELECT
        DivisionIEN,
        PatientIEN,
        PatientSSN,       
        LEFT(PatientLastName, 4) AS LName4,
        'I' AS InOutPatient,
        REPLACE(CONVERT(VARCHAR(10), PatientTransferDateTime, 120), '-', '') AS PatXferDate,
        '' AS PrimaryCareTeam,
        Gender,
        REPLACE(CONVERT(VARCHAR(10), BirthDateTime, 120), '-', '') AS PatientBirthDate,
        '' AS Religion,

        -- Employment Status Mapping
        CASE
            WHEN EmploymentStatus = 'EMPLOYED FULL TIME' THEN '1'
            WHEN EmploymentStatus = 'EMPLOYED PART TIME' THEN '2'
            WHEN EmploymentStatus = 'NOT EMPLOYED' THEN '3'
            WHEN EmploymentStatus = 'SELF EMPLOYED' THEN '4'
            WHEN EmploymentStatus = 'RETIRED' THEN '5'
            WHEN EmploymentStatus = 'ACTIVE MILITARY DUTY' THEN '6'
            ELSE '9'
        END AS AddressEmpStatus,

        '1' AS HealthInsurance,
        VAStateCode,
        County,
        Zip4,
        EligibilityVACode,
        VeteranFlag,
        'N' AS Vietnam,
        AgentOrangeExposureCode,
        IonizingRadiationCode,
        POWStatusCode,
        PeriodOfServiceCode,
        '' AS MeansTest,

        -- Marital Status Mapping
        CASE
            WHEN MaritalStatus = 'DIVORCED' THEN '1'
            WHEN MaritalStatus = 'MARRIED' THEN '2'
            WHEN MaritalStatus = 'WIDOWED' THEN '4'
            WHEN MaritalStatus = 'SEPARATED' THEN '5'
            WHEN MaritalStatus = 'NEVER MARRIED' THEN '6'
            WHEN MaritalStatus = 'UNKNOWN' THEN '7'
            ELSE ''
        END AS MaritalStatus,

        WardLocationIEN,
        'TreatSpec' AS TreatingSpecialty,
        StaffIEN,
        '12345678' AS MovementFileNum,
        '' AS PlaceholderDRG,
        '' AS Placeholder30,

        -- Extracting Time Component
        REPLACE(CONVERT(VARCHAR(8), PatientTransferDateTime, 108), ':', '') AS PatXferTime,

        '' AS PlaceholderPcProvider,
        '' AS PlaceholderRace,
        'PriWardProv' AS PrimaryWardProvider,
        '' AS MPI,
        '' AS Placeholder36,
        '' AS Placeholder37,
        '' AS Placeholder38,
        '' AS Placeholder39,
        '10' AS AdmissionEligibility,
        'U' AS MSTStatus,
        SHADFlag,
        '' AS Placeholder43,
        '' AS Placeholder44,
        EnrollmentLocation,
        '' AS Placeholder46,
        '' AS Placeholder47,
        '' AS Placeholder48,
        '' AS Placeholder49,
        'D' AS Dom,
        '?' AS EnrollmentCategory,
        '??' AS EnrollmentStatus,
        'N' AS EncounterSHAD,
        'N' AS PurpleHeart,
        'N' AS ObservationPt,
        
        AgentOrangeLocation,

        POWLocation,
        '' AS Placeholder62,
        '' AS Placeholder63,
            
        -- skipping down a bit...
        '' AS Placeholder70,
        SWAsiaCode,

        -- duplicate below, so commenting out
        -- pd.AgentOrangeExposureCode,

        '' AS Placeholder82,
        NPI,
        '' AS Placeholder84,

        -- duplicate below, so commenting out
        -- s.NPI,

        CountryCode,
        EligibilityStatus,
        CampLejeuneFlag,

        -- skipping down a bit...
        '' AS PlaceholderCerner,
        PatientICN,
        SIGI
        
    FROM ##AdmPatientExtract
    ORDER BY PatXferDate;
"""

# insert finalized records ito Extract database
ADM_INSERT_01 = """
    --
    -- Insert each finalized record into Extract.Data.ADM table
    --
    INSERT INTO [Data].ADM (
        DivisionIEN, PatientIEN, PatientSSN, LName4, InOutPatient, PatXferDate, PrimaryCareTeam, Gender,
        PatientBirthDate, Religion, AddressEmpStatus, HealthInsurance, VAStateCode, County, Zip4, EligibilityVACode,
        VeteranFlag, Vietnam, AgentOrangeExposureCode, IonizingRadiationCode, POWStatusCode, PeriodOfServiceCode,
        MeansTest, MaritalStatus, WardLocationIEN, TreatingSpecialty, StaffIEN, MovementFileNum, PlaceholderDRG,
        Placeholder30, PatXferTime, PlaceholderPcProvider, PlaceholderRace, PrimaryWardProvider, MPI, Placeholder36, Placeholder37,
        Placeholder38, Placeholder39, AdmissionEligibility, MSTStatus, SHADFlag, Placeholder43, Placeholder44,
        EnrollmentLocation, Placeholder46, Placeholder47, Placeholder48, Placeholder49, Dom, EnrollmentCategory,
        EnrollmentStatus, EncounterSHAD, PurpleHeart, ObservationPt, AgentOrangeLocation, POWLocation, Placeholder62,
        placeholder63, Placeholder70, SWAsiaCode, Placeholder82, NPI, Placeholder84, CountryCode, EligibilityStatus,
        CampLejeuneFlag, PlaceholderCerner, PatientICN, SIGI, RunStartDate, RunEndDate, RunSta3n, ExtractName,
        ExtractVersion, ExtractStatus, QueryTimestamp, QueryUser
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?
    )
"""
