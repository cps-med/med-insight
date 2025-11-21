# -----------------------------------------------------------------------
# constants_ascii_adm.py
# -----------------------------------------------------------------------
# Field specifications for ADM ASCII extract format
# -----------------------------------------------------------------------

ADM_EXTRACT_NAME = "ADM"
ADM_EXTRACT_VERSION = "1.0"

# Query to select from Extract database
ADM_QUERY_01 = """
    SELECT DivisionIEN, PatientIEN, PatientSSN, LName4, InOutPatient, PatXferDate, PrimaryCareTeam, Gender, PatientBirthDate, Religion, AddressEmpStatus, HealthInsurance, VAStateCode, County, Zip4, EligibilityVACode, VeteranFlag, Vietnam, AgentOrangeExposureCode, IonizingRadiationCode, POWStatusCode, PeriodOfServiceCode, MeansTest, MaritalStatus, WardLocationIEN, TreatingSpecialty, StaffIEN, MovementFileNum, PlaceholderDRG, Placeholder30, PatXferTime, MPI, Placeholder84, PurpleHeart, SIGI
    FROM Extract.Data.ADM
    WHERE RunSta3n = ? AND RunStartDate >= ? AND RunEndDate <= ? AND ExtractStatus = ?
"""

# Field specifications: (field_name, width, alignment, padding_char)
ADM_FIELD_SPECS = [
    ("DivisionIEN",            14, "left", " "),
    ("PatientIEN",             14, "left", " "),
    ("PatientSSN",             12, "left", " "),
    ("LName4",                  6, "left", " "),
    ("InOutPatient",            6, "left", " "),
    ("PatientXferDate",        14, "left", " "),
    ("PrimaryCareTeam",        14, "left", " "),
    ("Gender",                  8, "left", " "),
    ("PatientBirthDate",       14, "left", " "),
    ("Religion",               14, "left", " "),
    ("AddressEmpStatus",       14, "left", " "),
    ("HealthInsurance",        14, "left", " "),
    ("VAStateCode",            14, "left", " "),
    ("County",                 14, "left", " "),
    ("Zip4",                   14, "left", " "),
    ("EligibilityVACode",      14, "left", " "),
    ("VeteranFlag",             8, "left", " "),
    ("Vietnam",                 8, "left", " "),
    ("AgentOrangeExposureCode", 8, "left", " "),
    ("IonizingRadiationCode",   8, "left", " "),
    ("POWStatusCode",           8, "left", " "),
    ("PeriodOfServiceCode",     8, "left", " "),
    ("MeansTest",               8, "left", " "),
    ("MaritalStatus",           8, "left", " "),
    ("WardLocationIEN",        22, "left", " "),
    ("TreatingSpecialty",      14, "left", " "),
    ("StaffIEN",               14, "left", " "),
    ("MovementFileNum",        18, "left", " "),
    ("PlaceholderDRG",          8, "left", " "),
    ("Placeholder30",           8, "left", " "),
    ("PatXferTime",            10, "left", " "),

    ("MPI",                     8, "left", " "),

    ("Placeholder84",           6, "left", " "),
    ("PurpleHeart",             9, "left", " "),

    ("SIGI",                   14, "left", " ")
]

# Header row for ASCII file
ADM_HEADER_ROW = "DivisionIEN   PatientIEN    PatientSSN  LN4   IOP   PXDate        PriCareTeam   Gen     PtBirthDate   Religion      AddEmpStatus  HealthInsur   VAStateCode   County        Zip4          EligVACode    VetFlag Vietnam AOExpCd IRadCd  POWStCd POSCd   MnsTst  MarStat WardLocIEN            TreatSpec     StaffIEN      MovementFileNum   PHDRG   PH30    PtXferTm  MPI     PH84  PrplHrt  SIGI          "