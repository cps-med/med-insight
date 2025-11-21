"""
constants_sample_extract.py

Configuration constants and schema definitions for clinical data extract generation.
This module contains all constants, schemas, and lookup tables used by create_sample_extract.py.

Author: Chuck Sylvester
Created: 2025-08-09
Version: 2.0
"""

from datetime import datetime

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

DEFAULT_OUTPUT_DIR = "/Users/chuck/swdev/med/med-output/sample/dssext"
DEFAULT_RECORDS_PER_FILE = 10
BASE_PATIENT_NO = 100000
BASE_STAFF_NO = 2000
DATE_RANGE_START = datetime(2024, 1, 1)
DATE_RANGE_DAYS = 365

# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

# ADM: Hospital Admission Data
ADM_SCHEMA = [
    {'name': 'Facility', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Num_Dfn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ssn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Name', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Inout_Patient_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Day', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH007', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH008', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH009', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH010', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH011', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH012', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH013', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH014', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH015', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH016', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH017', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH018', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH019', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH020', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH021', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH022', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH023', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Marital_Status', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ward_Location', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Treating_Specialty', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Attending_Phys', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Movement_File_Num', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH029', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH030', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH032', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH033', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Ward_Prov', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH035', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH036', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH037', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH038', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH039', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admission_Elig', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH041', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH042', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH043', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH044', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH045', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH046', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH047', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH048', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH049', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Dom_Prrtp_Saartp', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH051', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH052', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Shad', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH054', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Observation_Pat_Ind', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Num', 'length': 18, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH057', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Production_Div_Cd', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH059', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Source_Of_Adm', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH061', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH062', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH063', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH064', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH065', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH066', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH067', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH068', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Cv', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH069', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Attending_Phys_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Ward_Prov_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH073', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH074', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH075', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Swac', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enc_Head_Neck_Ca', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Mst', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Radiation_Enc_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH080', 'length': 9, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH081', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH082', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Attending_Phys_Npi', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH084', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Ward_Prov_Npi', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admit_Op_Tx_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH087', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH088', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admit_Source', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ed_Disposition_Cd', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Icd_10_Cd', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH092', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Camp_Lej', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Sc', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH095', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH096', 'length': 14, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Division', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH098', 'length': 312, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH099', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH100', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
]

# CLI: Clinic Data
CLI_SCHEMA = [
    {'name': 'Facility', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Num_Dfn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ssn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Name', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Inout_Patient_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Day', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH007', 'length': 14, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Overbooked_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH009', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Treating_Spec', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH012', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH013', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH014', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider_Person_Cl', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH017', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH018', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH019', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH020', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH021', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH022', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH023', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH024', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH025', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH026', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH027', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH028', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH029', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH030', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH031', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH032', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH033', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH034', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH035', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH036', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Radiation_Enc_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH038', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Agent_Orange_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH040', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH041', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH042', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH043', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH044', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH045', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Elig', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH047', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Mst_Encounter_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH049', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH050', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH051', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH052', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH053', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH054', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH055', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH056', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Dom_Prrtp_Saartp', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH058', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH059', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH060', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH061', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH062', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Observation_Pat_Ind', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Num', 'length': 18, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH065', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Production_Div_Cd', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Appointment_Type', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Purpose_Of_Visit', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH069', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH070', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH071', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH072', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cboc_Status_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH074', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH075', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH076', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH077', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH078', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH079', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Cv', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH081', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH082', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Swac', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH084', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enc_Head_Neck_Ca', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH086', 'length': 9, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH087', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH088', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH089', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider_Npi', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH091', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Shad', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH093', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_1', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_1_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_1_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_2', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_2_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_2_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_3', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_3_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_3_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_4', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_4_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_4_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_5', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_5_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_5_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ed_Disposition_Cd', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Icd_10_Cd', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Icd_10_1', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Icd_10_2', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Icd_10_3', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Icd_10_4', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Sc', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH116', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_6', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_6_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_6_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_7', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_7_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Secondary_Prov_7_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH123', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Camp_Lej', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Primary_Pprocedure', 'length': 17, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH126', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH127', 'length': 14, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Clinic_Ien', 'length': 12, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'New_Feeder_Key', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Division', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_1', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_2', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_3', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_4', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_5', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_6', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_7', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_8', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_9', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_10', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_11', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_12', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_13', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_14', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_15', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_16', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_17', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_18', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_19', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_20', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_21', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_22', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_23', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_24', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_25', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH156', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Non_Count_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH158', 'length': 335, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admission_Date', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admission_Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH161', 'length': 172, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH162', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider_Taxonomy', 'length': 12, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider_Station', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Feeder_Location', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cprs_Provider_Stat', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH167', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
]

# DEM: Demographics Data
DEM_SCHEMA = [
    {'name': 'Facility', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Extract_Type', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Fiscal_Year', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Fiscal_Period', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Num', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ssn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Pseudo_SSN', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Name', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Master_Patient_Ind', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Date_Of_Birth', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Sex', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Veteran', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Eligibility', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Sc_Status', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'County', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'State', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Country', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Zip_Plus_4', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Period_Of_Service', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Purple_Heart', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Agent_Orange_Locat', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Agent_Orange_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Radiation_Status', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Sw_Asia_Conditions', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Head_Neck_Cancer_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Military_Sexual_Trau', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Oefoif', 'length': 9, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Oefoif_Return_Date', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Shad_Status', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Combat_Veteran_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cv_Status_Elig', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cv_Eligibility_End', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Combat_Veteran_Locat', 'length': 14, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Camp_Lejeune_Status', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Pow_Status', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Pow_Location', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Vietnam', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Type', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Eri', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patcat', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enroll_Category', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enroll_Status', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enroll_Location', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Enroll_Priority', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'User_Enrolee', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
]

# LAB: Laboratory Data
LAB_SCHEMA = [
    {'name': 'Facility', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Num_DFN', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ssn_Identifying_Num', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Name', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Inout_Patient_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Day', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Accession_Area', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Abbreviation', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Test', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Urgency_Of_Test', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Treating_Specialty', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Location', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Movement_File_Num', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'File', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Workload_Cd', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH018', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH019', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH020', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH021', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH022', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH023', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH024', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH025', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH026', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH027', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Dom_Prrtp_Saartp', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Observation_Pat_Ind', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Num', 'length': 18, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ordering_Stop_Cd', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ordering_Date', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Production_Division', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH034', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ordering_Provider_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH036', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH037', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH038', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Provider_Npi', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Loinc_Cd', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Lab_Billable_Proc', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Dss_Feeder_Key', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Data_Name', 'length': 40, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Data_Location', 'length': 12, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH045', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH046', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH047', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Pathologist', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Pathologist_Prov_Npi', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Cpt_Qty_Modify_1', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH052', 'length': 572, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH053', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH054', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
]

# MOV: Physical Movement Data
MOV_SCHEMA = [
    {'name': 'Facility', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Num_DFN', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Ssn', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Name', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Inout_Patient_Ind', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Day', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH007', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admission_Date', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Date', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Movement_File_Num', 'length': 8, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH011', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Losing_Ward', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Treating_Specialty', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Losing_Ward_Los', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH015', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Movement_Type', 'length': 3, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Mov_Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Gaining_Ward', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Admission_Time', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH020', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH021', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH022', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH023', 'length': 10, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Dom_Prrtp_Saartp', 'length': 1, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Observation_Pat_Ind', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Encounter_Num', 'length': 18, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Prov', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Pc_Team', 'length': 4, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Assoc_Prov', 'length': 11, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Production_Div_Cd', 'length': 6, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Pc_Prov_Pc', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH032', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH033', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Discharge_Pc_Prov_Np', 'length': 15, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH035', 'length': 5, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'Patient_Division', 'length': 7, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH037', 'length': 194, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH038', 'length': 20, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
    {'name': 'PH039', 'length': 2, 'data_type': 'str', 'justify': 'left', 'pad_char': ' '},
]

# Master dictionary to lookup schemas by data type
SCHEMAS = {
    'ADM': ADM_SCHEMA,
    'CLI': CLI_SCHEMA,
    'DEM': DEM_SCHEMA,
    'LAB': LAB_SCHEMA,
    'MOV': MOV_SCHEMA,
}

# =============================================================================
# LOOKUP TABLES FOR DATA GENERATION
# =============================================================================

# Medical diagnosis codes
DIAGNOSIS_CODES = [
    'J44.10', 'I25.10', 'N18.30', 'E11.9', 'F32.9', 'M84.552A',
    'M79.3', 'K59.00', 'R06.02', 'Z51.11', 'I10', 'M84.552B'
]

LOINC_CODES = [
    '8480-06', '8462-4', '2951-2', '3094-0',
    '30166-3', '30554-4', '32294-4', '30166-3'
]

LAB_DATA_NAMES = [
    'THYROID STIMULATING IMMUNOGLOB',
    'POLYCHROMASIA',
    'VON WILLEBRAND FACTOR MULTIMERS',
    'FATTY ACIDS, FREE',
    'AMPHETAMINES, SERUM',
    'THYROID STIMULATING IMMUNOGLOB'
]

LAB_DATA_LOCATIONS = [
    'CH;607766;1', 'CH;436455;1',
    'CH;412;1', 'CH;436475;1'
]

# Provider Taxonomy Codes (X12)
PROVIDER_TAXONOMY_CODES = [
    '207Q00000X', '207QG0300X', '261QM0800X',
    '363LF0000X', '251S00000X', '3747P1801X'
]

# VistA Sta3n values
STA3N_VALUES = ['442', '508', '516', '552']

# VistA Sta6a values
STA6A_VALUES = [
    '442', '442AA', '442AB',
    '508', '508AA', '508AB',
    '516', '516AA', '516BB',
    '552', '552AA', '552BB'
]

# Doctor names
DOCTOR_NAMES = [
    'SMITH_MD', 'JONES_MD', 'BROWN_MD', 'DAVIS_MD', 'WILSON_MD',
    'MILLER_MD', 'MOORE_MD', 'TAYLOR_MD', 'CLARK_MD', 'WHITE_MD'
]

# Radiology modalities and related data
MODALITIES = ['CT', 'MRI', 'XRAY', 'US', 'NM', 'PET', 'MAMM']
BODY_PARTS = ['CHEST', 'HEAD', 'ABDOMEN', 'PELVIS', 'SPINE', 'EXTREMITY', 'CARDIAC']
RADIOLOGISTS = ['RAD001', 'RAD002', 'RAD003', 'RAD004', 'RAD005']

# Laboratory test definitions
LAB_TESTS = [
    {'code': 'CBC001', 'name': 'COMPLETE_CBC', 'ref_range': '4.5-11.0', 'unit': 'K/uL'},
    {'code': 'CMP002', 'name': 'BASIC_METABOLIC', 'ref_range': '136-145', 'unit': 'mEq/L'},
    {'code': 'TSH003', 'name': 'THYROID_STIM', 'ref_range': '0.4-4.0', 'unit': 'mIU/L'},
    {'code': 'PSA004', 'name': 'PROSTATE_SPEC', 'ref_range': '0-4.0', 'unit': 'ng/mL'},
    {'code': 'HBA1C5', 'name': 'HEMOGLOBIN_A1C', 'ref_range': '4.0-5.6', 'unit': '%'}
]

# Demographics lookup tables
FIRST_NAMES = [
    'JOHN', 'MARY', 'ROBERT', 'PATRICIA', 'MICHAEL', 
    'JENNIFER', 'WILLIAM', 'LINDA', 'DAVID', 'ELIZABETH'
]

LAST_NAMES = [
    'SMITH', 'JOHNSON', 'WILLIAMS', 'JONES', 'BROWN',
    'DAVIS', 'MILLER', 'WILSON', 'MOORE', 'TAYLOR'
]

ADDRESSES = [
    '123 MAIN ST', '456 ELM AVE', '789 OAK DR', '321 PINE RD', '654 CEDAR LN',
    '987 MAPLE WAY', '147 BIRCH CT', '258 WILLOW ST', '369 SPRUCE AVE', '741 POPLAR DR'
]

CITIES = [
    'SPRINGFIELD', 'FRANKLIN', 'MADISON', 'GEORGETOWN', 'CLINTON',
    'RIVERSIDE', 'FAIRVIEW', 'MIDWAY', 'OAKDALE', 'PLEASANT VALLEY'
]

STATES = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']

ZIP_CODES = ['90210', '10001', '33101', '60601', '19101', '30301', '27601', '48201', '77001', '94102']

PHONE_PREFIXES = ['555', '444', '333', '222', '111']

COMBAT_VET_LOCATION = [
    'WWI', 'WWII-EUROPE', 'WWII-PACIFIC',
    'KOREAN', 'VIETNAM', 'OTHER', ' ',
    'PERSIAN GULF', 'YUGOSLAVIA', ' '
]

PATIENT_CATEGORY = [
    'AD', 'ADD', 'FNRS', 'RET', 'RETD',
    'RES', 'REC', 'TDRL', 'TFL'
]