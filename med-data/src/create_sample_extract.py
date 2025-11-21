"""
create_sample_extract.py

This program creates DSS file layout schema files for an initial set of extracts.

It also creates ASCII fixed-length text files that simulate clinical data extracts
for mainframe/SAS systems. It supports multiple data types with predefined schemas.

Author: Chuck Sylvester
Created: 2025-08-09
Version: 1.0

USAGE:
------
1. Run the entire program to create all sample files:
   python create_sample_extract.py

2. Import and use specific functions:
   from create_sample_extract import create_sample_extract_file, print_schema_info
   
   # Create a single extract file
   create_sample_extract_file('ADM', 'my_admission_data.txt', 50)
   
   # View schema information
   print_schema_info('ADM')
   
   # View all available schemas
   print_all_schemas()

3. Customize for your needs:
   - Modify configuration constants at top of file
   - Modify schema definitions (ADM_SCHEMA, CLI_SCHEMA, etc.) to match your requirements
   - Add new data types by creating new schemas and generator functions
   - Adjust sample data generation logic in generate_*_field_value() functions

EXAMPLES:
---------
# Create 25 admission records
create_sample_extract_file('ADM', 'admission_extract.txt', 25)

# Create 10 radiology records  
create_sample_extract_file('RAD', 'radiology_extract.txt', 10)

# View lab schema details
print_schema_info('LAB')

FILES CREATED:
--------------
When run as main program, creates files in timestamped directory:
- extract_files_YYYYMMDD_HHMMSS/adm_extract.txt
- extract_files_YYYYMMDD_HHMMSS/rad_extract.txt  
- extract_files_YYYYMMDD_HHMMSS/lab_extract.txt
"""

import argparse
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

# Import configuration constants and schemas
from constants_sample_extract import *

def validate_schema(schema, data_type):
    """
    Validate schema structure and data types.
    
    Args:
        schema: List of field definition dictionaries
        data_type: String indicating data type
    
    Returns:
        bool: True if valid, False otherwise
    """
    required_keys = ['name', 'length', 'data_type', 'justify', 'pad_char']
    
    for i, field_def in enumerate(schema):
        # Check required keys
        for key in required_keys:
            if key not in field_def:
                print(f"Error: Missing '{key}' in {data_type} schema field {i}")
                return False
        
        # Validate data types
        if field_def['data_type'] not in ['str', 'int', 'float']:
            print(f"Error: Invalid data_type '{field_def['data_type']}' in {data_type} schema")
            return False
        
        # Validate justification
        if field_def['justify'] not in ['left', 'right']:
            print(f"Error: Invalid justify '{field_def['justify']}' in {data_type} schema")
            return False
        
        # Validate length
        if not isinstance(field_def['length'], int) or field_def['length'] <= 0:
            print(f"Error: Invalid length '{field_def['length']}' in {data_type} schema")
            return False
    
    return True


def format_field_value(value, field_def):
    """
    Format a value according to field definition with enhanced validation.
    
    Args:
        value: The value to format
        field_def: Dictionary containing field definition (length, justify, pad_char)
    
    Returns:
        str: Formatted string with proper length, justification, and padding
    """
    # Handle None values
    if value is None:
        value = ""
    
    # Convert to string
    str_value = str(value)
    
    # Truncate if too long
    if len(str_value) > field_def['length']:
        str_value = str_value[:field_def['length']]
    
    # Apply justification and padding
    if field_def['justify'] == 'left':
        return str_value.ljust(field_def['length'], field_def['pad_char'])
    else:  # right
        return str_value.rjust(field_def['length'], field_def['pad_char'])


def create_header_row(schema, truncate_names=True):
    """
    Create header row with column names, optionally truncating if necessary.
    
    Args:
        schema: List of field definition dictionaries
        truncate_names: Boolean to control whether field names are truncated to fit field width
    
    Returns:
        str: Formatted header row string
    """
    header_fields = []
    for field_def in schema:
        column_name = field_def['name']
        
        if truncate_names:
            # Truncate field names to fit field width and apply padding
            formatted_header = format_field_value(column_name, field_def)
        else:
            # Use full field names without truncation
            # This means header may not align with fixed-width data columns
            header_fields.append(column_name)
            continue
        
        header_fields.append(formatted_header)
    
    # Join with appropriate separator
    if truncate_names:
        # No separator needed for fixed-width format
        return ''.join(header_fields)
    else:
        # Use tab separator for readability when using full field names
        return '\t'.join(header_fields)


def generate_patient_no(record_index):
    """Generate consistent patient ID across all data types."""
    return f"PAT{BASE_PATIENT_NO + record_index:06d}"


def generate_staff_no(record_index):
    """Generate consistent patient ID across all data types."""
    return f"STF{BASE_STAFF_NO + record_index:04d}"


def generate_random_date(days_offset_range=None):
    """
    Generate random date within specified range.
    
    Args:
        days_offset_range: Tuple of (min_days, max_days) from base date
    
    Returns:
        str: Date in YYYYMMDD format
    """
    if days_offset_range is None:
        random_days = random.randint(0, DATE_RANGE_DAYS)
    else:
        random_days = random.randint(days_offset_range[0], days_offset_range[1])
    
    sample_date = DATE_RANGE_START + timedelta(days=random_days)
    return sample_date.strftime("%Y%m%d")


def generate_random_time():
    """Generate random time in HHMMSS format during business hours."""
    hour = random.randint(7, 18)  # 7 AM to 6 PM
    minute = random.randint(0, 59)
    return f"{hour:02d}{minute:02d}00"


def generate_sample_data(schema, data_type, num_records=5):
    """
    Generate sample data records based on data type with improved correlation.
    
    Args:
        schema: List of field definition dictionaries
        data_type: String indicating data type ('ADM', 'RAD', 'LAB', 'DEM', 'CLI')
        num_records: Number of records to generate
    
    Returns:
        list: List of formatted record strings
    """
    records = []
    
    for i in range(num_records):
        # Generate correlated data for this record
        patient_no = generate_patient_no(i)
        staff_no = generate_staff_no(i)
        base_date = generate_random_date()
        
        record_fields = []
        
        for field_def in schema:
            field_name = field_def['name']
            
            # Generate sample data based on data type and field name
            if data_type == 'ADM':
                value = generate_adm_field_value(field_name, i, patient_no, staff_no, base_date)
            elif data_type == 'CLI':
                value = generate_cli_field_value(field_name, i, patient_no, staff_no, base_date)
            elif data_type == 'DEM':
                value = generate_dem_field_value(field_name, i, patient_no, staff_no, base_date)
            elif data_type == 'LAB':
                value = generate_lab_field_value(field_name, i, patient_no, staff_no, base_date)
            elif data_type == 'MOV':
                value = generate_mov_field_value(field_name, i, patient_no, staff_no, base_date)
            else:
                value = f"DATA{i}"
            
            formatted_field = format_field_value(value, field_def)
            record_fields.append(formatted_field)
        
        records.append(''.join(record_fields))
    
    return records


# Global dictionary to store correlated patient data for each record
_patient_data_cache = {}


def generate_adm_field_value(field_name, record_index, patient_no, staff_no, base_date):
    """Generate sample values for ADM (admission) fields with correlation."""
    
    # Generate correlated SSN and NAME data for this record if not already cached
    if record_index not in _patient_data_cache:
        # Randomly select SSN and corresponding NAME
        ssn_name_pairs = [
            ('111111111', 'SMITH'),
            ('222222222', 'JOHNSOB'), 
            ('333333333', 'BOONE')
        ]
        selected_ssn, selected_name = random.choice(ssn_name_pairs)
        _patient_data_cache[record_index] = {
            'ssn': selected_ssn,
            'name': selected_name
        }
    
    if field_name == str.title('FACILITY'):
        return '1'
    elif field_name == str.title('PATIENT_NUM_DFN'):
        return patient_no
    elif field_name == str.title('SSN'):
        return _patient_data_cache[record_index]['ssn']
    elif field_name == str.title('NAME'):
        return _patient_data_cache[record_index]['name']
    elif field_name == str.title('INOUT_PATIENT_IND'):
        return random.choice(['I', 'O'])
    elif field_name == str.title('DAY'):
        return base_date
    elif field_name == str.title('MARITAL_STATUS'):
        return '333'
    elif field_name == str.title('WARD_LOCATION'):
        return '223344'
    elif field_name == str.title('TREATING_SPECIALTY'):
        return '888888'
    elif field_name == str.title('ATTENDING_PHYS'):
        return '125125'
    elif field_name == str.title('MOVEMENT_FILE_NUM'):
        return '12345678'
    elif field_name == str.title('TIME'):
        return generate_random_time()
    elif field_name == str.title('PRIMARY_WARD_PROV'):
        return '2203618'
    elif field_name == str.title('ADMISSION_ELIG'):
        return random.randint(1, 10)
    elif field_name == str.title('DOM_PRRTP_SAARTP'):
        return random.choice(['P', 'D', 'S', 'T', 'H', 'A', 'B', 'C'])
    elif field_name == str.title('ENCOUNTER_SHAD'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('OBSERVATION_PAT_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_NUM'):
        return '397426621140701I'
    elif field_name == str.title('PRODUCTION_DIV_CD'):
        return '607BU'
    elif field_name == str.title('SOURCE_OF_ADM'):
        return random.choice(['1', '2', '3', '4', '5'])
    elif field_name == str.title('ENCOUNTER_CV'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ATTENDING_PHYS_PC'):
        return random.choice(['V181004', 'V115500', 'V246002'])
    elif field_name == str.title('PRIMARY_WARD_PROV_PC'):
        return random.choice(['V181004', 'V115500', 'V246002'])
    elif field_name == str.title('ENCOUNTER_SWAC'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENC_HEAD_NECK_CA'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_MST'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('RADIATION_ENC_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ATTENDING_PHYS_NPI'):
        return staff_no
    elif field_name == str.title('PRIMARY_WARD_PROV_NPI'):
        return staff_no
    elif field_name == str.title('ADMIT_OP_TX_IND'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('ADMIT_SOURCE'):
        return 'AAA'
    elif field_name == str.title('ED_DISPOSITION_CD'):
        return random.choice(['A', 'D', 'E', 'L', 'R', 'T', 'U', 'N'])
    elif field_name == str.title('PRIMARY_ICD_10_CD'):
        return random.choice(DIAGNOSIS_CODES)
    elif field_name == str.title('ENCOUNTER_CAMP_LEJ'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_SC'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('PATIENT_DIVISION'):
        return random.choice(['442', '508', '516', '552'])
    else:
        return ' '


def generate_cli_field_value(field_name, record_index, patient_no, staff_no, base_date):
    """Generate sample values for CLI (clinic) fields with correlation."""

    # Generate correlated SSN and NAME data for this record if not already cached
    if record_index not in _patient_data_cache:
        # Randomly select SSN and corresponding NAME
        ssn_name_pairs = [
            ('111111111', 'SMITH'),
            ('222222222', 'JOHNSON'), 
            ('333333333', 'BOONE')
        ]
        selected_ssn, selected_name = random.choice(ssn_name_pairs)
        _patient_data_cache[record_index] = {
            'ssn': selected_ssn,
            'name': selected_name
        }
    
    if field_name == str.title('FACILITY'):
        return '1'
    elif field_name == str.title('PATIENT_NUM_DFN'):
        return patient_no
    elif field_name == str.title('SSN'):
        return _patient_data_cache[record_index]['ssn']
    elif field_name == str.title('NAME'):
        return _patient_data_cache[record_index]['name']
    elif field_name == str.title('INOUT_PATIENT_IND'):
        return random.choice(['I', 'O'])
    elif field_name == str.title('DAY'):
        return base_date
    elif field_name == str.title('OVERBOOKED_IND'):
        return random.choice(['O', ' '])
    elif field_name == str.title('TREATING_SPEC'):
        return '888888'
    elif field_name == str.title('TIME'):
        return generate_random_time()
    elif field_name == str.title('PROVIDER'):
        return staff_no
    elif field_name == str.title('PROVIDER_PERSON_CL'):
        return random.choice(['V181004', 'V115500', 'V246002'])
    elif field_name == str.title('RADIATION_ENC_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('AGENT_ORANGE_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_ELIG'):
        return 'ELG'
    elif field_name == str.title('MST_ENCOUNTER_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('DOM_PRRTP_SAARTP'):
        return random.choice(['P', 'D', 'S', 'T', 'H', 'A', 'B', 'C'])
    elif field_name == str.title('OBSERVATION_PAT_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_NUM'):
        return '397426621140701I'
    elif field_name == str.title('PRODUCTION_DIV_CD'):
        return random.choice(['442', '508', '516', '552'])
    elif field_name == str.title('APPOINTMENT_TYPE'):
        return random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    elif field_name == str.title('PURPOSE_OF_VISIT'):
        return random.choice(['1', '2', '3', '4'])
    elif field_name == str.title('CBOC_STATUS_IND'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('ENCOUNTER_CV'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('ENCOUNTER_SWAC'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('ENC_HEAD_NECK_CA'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('PROVIDER_NPI'):
        return staff_no
    elif field_name == str.title('ENCOUNTER_SHAD'):
        return random.choice(['Y', 'N'])
    elif str.title('SECONDARY_PROV') in field_name:  # slight twist to catch all in pattern
        return 'SECPROV'
    elif field_name == str.title('ED_DISPOSITION_CD'):
        return random.choice(['A', 'D', 'E', 'L', 'R', 'T', 'U', 'N'])
    elif field_name == str.title('PRIMARY_ICD_10_CD'):
        return random.choice(DIAGNOSIS_CODES)
    elif str.title('SECONDRY_ICD_10') in field_name:  # slight twist to catch all in pattern
        return random.choice(DIAGNOSIS_CODES)
    elif field_name == str.title('ENCOUNTER_SC'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_CAMP_LEJ'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('PRIMARY_PROCEDURE'):
        return random.choice(DIAGNOSIS_CODES)
    elif field_name == str.title('CLINIC_IEN'):
        return 'CL44440001'
    elif field_name == str.title('NEW_FEEDER_KEY'):
        return '103801030CDRC021'
    elif field_name == str.title('PATIENT_DIVISION'):
        return random.choice(['442', '508', '516', '552'])
    elif str.title('CPT_QTY_MODIFY') in field_name:    # slight twist to catch pattern
        return random.choice(['AAA-AAA', 'BBB-BBB', 'CCC-CCC', 'DDD-DDD'])
    elif field_name == str.title('NON_COUNT_IND'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('ADMISSION_DATE'):
        return base_date
    elif field_name == str.title('ADMISSION_TIME'):
        return generate_random_time()
    elif field_name == str.title('PROVIDER_TAXONOMY'):
        return random.choice(PROVIDER_TAXONOMY_CODES)
    elif field_name == str.title('PROVIDER_STATION'):
        return random.choice(['442', '508', '516', '552'])
    elif field_name == str.title('FEEDER_LOCATION'):
        return 'FDLOCSTP'
    elif field_name == str.title('CPRS_PROVIDER_STAT'):
        return random.choice(['442', '508', '516', '552'])
    else:
        return ' '


def generate_dem_field_value(field_name, record_index, patient_no, staff_no, base_date):
    """Generate sample values for DEM (demographics) fields with correlation."""
    
    # Create unique cache key for DEM data type to avoid conflicts
    dem_cache_key = f"DEM_{record_index}"
    
    # Generate correlated demographic data for this record if not already cached
    if dem_cache_key not in _patient_data_cache:
        # Select correlated names and SSN
        ssn_name_pairs = [
            ('111111111', 'SMITH'),
            ('222222222', 'JOHNSON'), 
            ('333333333', 'BOONE')
        ]
        selected_ssn, selected_last_name = random.choice(ssn_name_pairs)
        selected_first_name = random.choice(FIRST_NAMES)
        
        # Generate correlated address info
        address = random.choice(ADDRESSES)
        city = random.choice(CITIES)
        state = random.choice(STATES)
        zip_code = random.choice(ZIP_CODES)
        
        # Generate phone number
        phone_prefix = random.choice(PHONE_PREFIXES)
        phone_suffix = f"{random.randint(0, 9999):04d}"
        
        _patient_data_cache[dem_cache_key] = {
            'ssn': selected_ssn,
            'first_name': selected_first_name,
            'last_name': selected_last_name,
            'full_name': f"{selected_first_name} {selected_last_name}",
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'phone_number': f"{phone_prefix}{phone_suffix}"
        }
    
    if field_name == str.title('FACILITY'):
        return random.choice(STA6A_VALUES)
    elif field_name == str.title('EXTRACT_TYPE'):
        return 'DEM'
    elif field_name == str.title('FISCAL_YEAR'):
        return '2025'
    elif field_name == str.title('FISCAL_PERIOD'):
        return '06'
    elif field_name == str.title('PATIENT_NUM'):
        return patient_no
    elif field_name == str.title('SSN'):
        return _patient_data_cache[dem_cache_key]['ssn']
    elif field_name == str.title('NAME'):
        return _patient_data_cache[record_index]['name']
    elif field_name == str.title('MASTER_PATIENT_IND'):
        return f"{BASE_PATIENT_NO + record_index}V{random.randint(0, 999999):06d}"
    elif field_name == str.title('DATE_OF_BIRTH'):
        return random.choice(['19960801', '19710315', '19530705', '20001225'])
    elif field_name == str.title('SEX'):
        return random.choice(['M', 'F', 'M'])
    elif field_name == str.title('VETERAN'):
        return random.choice(['Y', 'N', 'Y'])
    elif field_name == str.title('ELIGIBILITY'):
        return random.choice(['111', '222', '333', '444'])
    elif field_name == str.title('SC_STATUS'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('COUNTY'):
        return f"{random.randint(1, 999):03d}"
    elif field_name == str.title('STATE'):
        return f"{random.randint(1, 55):02d}"
    elif field_name == str.title('COUNTRY'):
        return random.choice(['USA', 'CAN', 'USA', 'MEX', 'USA'])
    elif field_name == str.title('ZIP_PLUS_4'):
        return f"{random.randint(11234, 88888)}-0000"
    elif field_name == str.title('PERIOD_OF_SERVICE'):
        return random.randint(1, 9)
    elif field_name == str.title('PURPLE_HEART'):
        return random.choice(['Y', 'N', 'N'])
    elif field_name == str.title('AGENT_ORANGE_LOCAT'):
        return random.choice(['B', 'K', 'V', 'O', ' '])
    elif field_name == str.title('AGENT_ORANGE_IND'):
        return random.choice(['Y', ' '])
    elif field_name == str.title('RADIATION_STATUS'):
        return random.choice(['1', '2', '3', '4', '5', '6', '6', 'U'])
    elif field_name == str.title('SW_ASIA_CONDITIONS'):
        return random.choice(['Y', 'N', 'U'])
    elif field_name == str.title('HEAD_NECK_CANCER_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('MILITARY_SEXUAL_TRAU'):
        return random.choice(['Y', 'N', 'U', 'D'])
    elif field_name == str.title('OEFOIF'):
        return random.choice(['OEF', 'OIF', 'OEFOIF', 'OIFOEF', 'UNK'])
    elif field_name == str.title('OEFOIF_RETURN_DATE'):
        return random.choice(['20090808', ''])
    elif field_name == str.title('SHAD_STATUS'):
        return random.choice(['Y', 'N', 'U'])
    elif field_name == str.title('COMBAT_VETERAN_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('CV_STATUS_ELIG'):
        return random.choice(['Y', 'E'])
    elif field_name == str.title('CV_ELIGIBILITY_END'):
        return random.choice(['20100213', ''])
    elif field_name == str.title('COMBAT_VETERAN_LOCAT'):
        return random.choice(COMBAT_VET_LOCATION)
    elif field_name == str.title('CAMP_LEJEUNE_STATUS'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('POW_STATUS'):
        return random.choice(['Y', 'N', 'U'])
    elif field_name == str.title('POW_LOCATION'):
        return random.choice([' ', '1', '2', '3', '4', '5', '6', ' '])
    elif field_name == str.title('VIETNAM'):
        return random.choice(['Y', 'N', 'U'])
    elif field_name == str.title('PATIENT_TYPE'):
        return random.choice(['AC', 'AL', 'CO', 'EM', 'IN', 'MI', 'NO', 'NS', 'SC', 'TR'])
    elif field_name == str.title('ERI'):
        return random.choice(['K', 'P', ' '])
    elif field_name == str.title('PATCAT'):
        return random.choice(PATIENT_CATEGORY)
    elif field_name == str.title('ENROLL_CATEGORY'):
        return 'E'
    elif field_name == str.title('ENROLL_STATUS'):
        return f"{random.randint(1, 5):02d}"
    elif field_name == str.title('ENROLL_LOCATION'):
        return random.choice(STA6A_VALUES)
    elif field_name == str.title('ENROLL_PRIORITY'):
        return random.randint(1, 8)
    elif field_name == str.title('USER_ENROLEE'):
        return random.choice(['U', ' '])
    else:
        return ' '


def generate_lab_field_value(field_name, record_index, patient_no, staff_no, base_date):
    """Generate sample values for LAB (laboratory) fields with correlation."""

    # Generate correlated SSN and NAME data for this record if not already cached
    if record_index not in _patient_data_cache:
        # Randomly select SSN and corresponding NAME
        ssn_name_pairs = [
            ('111111111', 'SMITH'),
            ('222222222', 'JOHNSON'), 
            ('333333333', 'BOONE')
        ]
        selected_ssn, selected_name = random.choice(ssn_name_pairs)
        _patient_data_cache[record_index] = {
            'ssn': selected_ssn,
            'name': selected_name
        }

    if field_name == str.title('FACILITY'):
        return f"{random.choice(STA3N_VALUES)}LAB"
    if field_name == str.title('PATIENT_NUM_DFN'):
        return patient_no
    elif field_name == str.title('SSN_IDENTIFYING_NUM'):
        return _patient_data_cache[record_index]['ssn']
    elif field_name == str.title('NAME'):
        return _patient_data_cache[record_index]['name']
    elif field_name == str.title('INOUT_PATIENT_IND'):
        return random.choice(['I', 'O'])
    elif field_name == str.title('DAY'):
        return base_date
    elif field_name == str.title('ACCESSION_AREA'):
        return f"{random.randint(111, 888):03d}"
    elif field_name == str.title('ABBREVIATION'):
        return random.choice(['OSR', 'ANC', 'LCO', 'LITH', 'DM', 'LC', 'MOL', 'SOLEX', 'SCHEM', 'TOX'])
    elif field_name == str.title('TEST'):
        return f"{random.randint(3000, 7999):04d}"
    elif field_name == str.title('URGENCY_OF_TEST'):
        return f"{random.randint(1, 99):02d}"
    elif field_name == str.title('TREATING_SPECIALTY'):
        return f"{random.randint(1, 99):02d}"
    elif field_name == str.title('LOCATION'):
        return '000000000000000000'
    elif field_name == str.title('PROVIDER'):
        return f"2{staff_no}"
    elif field_name == str.title('MOVEMENT_FILE_NUM'):
        return '12345678'
    elif field_name == str.title('FILE'):
        return random.randint(5, 55555)
    elif field_name == str.title('TIME'):
        return generate_random_time()
    elif field_name == str.title('WORKLOAD_CD'):
        return f"{random.randint(81000, 89999)}.{random.randint(8100, 8999)}"
    elif field_name == str.title('DOM_PRRTP_SAARTP'):
        return random.choice(['P', 'D', 'S', 'T', 'H', 'A', 'B', 'C'])
    elif field_name == str.title('OBSERVATION_PAT_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_NUM'):
        return '397426621140701I'
    elif field_name == str.title('ORDERING_STOP_CD'):
        return '323'
    elif field_name == str.title('ORDERING_DATE'):
        return base_date
    elif field_name == str.title('PRODUCTION_DIVISION'):
        return random.choice(STA3N_VALUES)
    elif field_name == str.title('ORDERING_PROVIDER_PC'):
        return random.choice(['V181004', 'V115500', 'V246002'])
    elif field_name == str.title('PROVIDER_NPI'):
        return f"1528664885{record_index:02}"
    elif field_name == str.title('LOINC_CD'):
        return random.choice(LOINC_CODES)
    elif field_name == str.title('LAB_BILLABLE_PROC'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('DSS_FEEDER_KEY'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('DATA_NAME'):
        return random.choice(LAB_DATA_NAMES)
    elif field_name == str.title('DATA_LOCATION'):
        return random.choice(LAB_DATA_LOCATIONS)
    elif field_name == str.title('PATHOLOGIST'):
        return f"48{staff_no}"
    elif field_name == str.title('PATHOLOGIST_PROV_NPI'):
        return f"252535{record_index:03}"
    elif str.title('CPT_QTY_MODIFY') in field_name:  # sight twist to get all in pattern
        return random.choice(['AAA-AAA', 'BBB-BBB', 'CCC-CCC', 'DDD-DDD'])
    else:
        return ' '

""" (other interesting transformations)
    elif field_name == 'DISCHARGE_DATE':
        # Generate discharge date 1-30 days after order
        order_date = datetime.strptime(base_date, "%Y%m%d")
        discharge_days = random.randint(1, 30)
        discharge_date = order_date + timedelta(days=discharge_days)
        return discharge_date.strftime("%Y%m%d")
    elif field_name == 'LENGTH_OF_STAY':
        return random.randint(1, 30)
    elif field_name == 'ATTENDING_DOC':
        return random.choice(DOCTOR_NAMES)
"""


def generate_mov_field_value(field_name, record_index, patient_no, staff_no, base_date):
    """Generate sample values for MOV (physical movement) fields with correlation."""

    # Generate correlated SSN and NAME data for this record if not already cached
    if record_index not in _patient_data_cache:
        # Randomly select SSN and corresponding NAME
        ssn_name_pairs = [
            ('111111111', 'SMITH'),
            ('222222222', 'JOHNSOB'), 
            ('333333333', 'BOONE')
        ]
        selected_ssn, selected_name = random.choice(ssn_name_pairs)
        _patient_data_cache[record_index] = {
            'ssn': selected_ssn,
            'name': selected_name
        }

    if field_name == str.title('FACILITY'):
        return '1'
    elif field_name == str.title('PATIENT_NUM_DFN'):
        return patient_no
    elif field_name == str.title('SSN'):
        return _patient_data_cache[record_index]['ssn']
    elif field_name == str.title('NAME'):
        return _patient_data_cache[record_index]['name']
    elif field_name == str.title('INOUT_PATIENT_IND'):
        return random.choice(['I', 'O'])
    elif field_name == str.title('DAY'):
        return base_date
    elif field_name == str.title('ADMISSION_DATE'):
        return base_date
    elif field_name == str.title('DISCHARGE_DATE'):
        return base_date
    elif field_name == str.title('MOVEMENT_FILE_NUM'):
        return '12345678'
    elif field_name == str.title('LOSING_WARD'):
        return '223344'
    elif field_name == str.title('TREATING_SPECIALTY'):
        return '888888'
    elif field_name == str.title('LOSING_WARD_LOS'):
        return 'LLOS'
    elif field_name == str.title('MOVEMENT_TYPE'):
        return '101'
    elif field_name == str.title('MOV_TIME'):
        return generate_random_time()
    elif field_name == str.title('GAINING_WARD'):
        return '222001'
    elif field_name == str.title('ADMISSION_TIME'):
        return generate_random_time()
    elif field_name == str.title('DOM_PRRTP_SAARTP'):
        return random.choice(['P', 'D', 'S', 'T', 'H', 'A', 'B', 'C'])
    elif field_name == str.title('OBSERVATION_PAT_IND'):
        return random.choice(['Y', 'N'])
    elif field_name == str.title('ENCOUNTER_NUM'):
        return '397426621140701I'
    elif field_name == str.title('DISCHARGE_PROV'):
        return '2464200001'
    elif field_name == str.title('DISCHARGE_Pc_Team'):
        return '4444'
    elif field_name == str.title('DISCHARGE_ASSOC_PROV'):
        return '2464200002'
    elif field_name == str.title('PRODUCTION_DIV_CD'):
        return '607BU'
    elif field_name == str.title('DISCHARGE_PC_PROV_PC'):
        return random.choice(['V181004', 'V115500', 'V246002'])
    elif field_name == str.title('DISCHARGE_PC_PROV_NP'):
        return staff_no
    elif field_name == str.title('PATIENT_DIVISION'):
        return random.choice(['442', '508', '516', '552'])
    else:
        return ' '


def create_output_directory():
    """
    Create timestamped output directory.
    
    Returns:
        Path: Path object for the created directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"{DEFAULT_OUTPUT_DIR}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def create_sample_extract_file(data_type, filename, num_records=DEFAULT_RECORDS_PER_FILE, output_dir=None, truncate_names=True):
    """
    Create a complete sample extract file with header and data.
    
    Args:
        data_type: String indicating data type ('ADM', 'RAD', 'LAB')
        filename: Output filename for the extract file
        num_records: Number of data records to generate
        output_dir: Directory to write file (if None, uses current directory)
        truncate_names: Boolean to control whether header field names are truncated to fit field width
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Validate data type
    if data_type not in SCHEMAS:
        print(f"Error: Unknown data type '{data_type}'. Available types: {list(SCHEMAS.keys())}")
        return False
    
    schema = SCHEMAS[data_type]
    
    # Validate schema
    if not validate_schema(schema, data_type):
        print(f"Error: Invalid schema for data type '{data_type}'")
        return False
    
    # Determine output file path
    if output_dir:
        output_path = Path(output_dir) / filename
    else:
        output_path = Path(filename)
    
    try:
        # Create header row
        header = create_header_row(schema, truncate_names)
        
        # Generate sample data
        print(f"Generating {num_records} sample {data_type} records...")
        data_records = generate_sample_data(schema, data_type, num_records)
        
        # Write to file
        with open(output_path, 'w') as f:
            # Write header
            f.write(header + '\n')
            
            # Write data records
            for record in data_records:
                f.write(record + '\n')
        
        print(f"✓ Sample {data_type} extract file '{output_path}' created successfully!")
        print(f"  Records: {num_records} | Total length: {len(header)} characters per record")
        
        # Show sample of output
        print(f"  Header: {header}")
        if data_records:
            print(f"  Sample: {data_records[0]}")
        
        return True
        
    except Exception as e:
        print(f"Error creating extract file '{filename}': {e}")
        return False


def print_schema_info(data_type, truncate_names=True):
    """
    Print detailed schema information for verification.
    
    Args:
        data_type: String indicating data type ('ADM', 'RAD', 'LAB')
        truncate_names: Boolean to control whether field names are truncated to fit field width
    """
    if data_type not in SCHEMAS:
        print(f"Error: Unknown data type '{data_type}'. Available types: {list(SCHEMAS.keys())}")
        return
    
    schema = SCHEMAS[data_type]
    
    print(f"\n{data_type} Schema Definition:")
    print("=" * 80)
    print(f"{'Field Name':<22} | {'Len':<4} | {'Type':<5} | {'Just':<5} | {'Pad':<4} | {'Header Display'}")
    print("-" * 80)
    
    total_length = 0
    for field_def in schema:
        # Check if field name exceeds the field length
        field_name = field_def['name']
        field_length = field_def['length']
        
        # Optionally truncate header display if field name is too long
        if truncate_names and len(field_name) > field_length:
            header_display = field_name[:field_length]
        else:
            header_display = field_name
            
        print(f"{field_def['name']:<22} | {field_def['length']:<4} | {field_def['data_type']:<5} | {field_def['justify']:<5} | '{field_def['pad_char']}'  | '{header_display}'")
        total_length += field_def['length']
    
    print("-" * 80)
    print(f"Total record length: {total_length} characters")
    print()


def print_all_schemas(truncate_names=True):
    """
    Print information for all available schemas.
    
    Args:
        truncate_names: Boolean to control whether field names are truncated to fit field width
    """
    print("Available Data Types and Schemas:")
    print("=" * 80)
    for data_type in sorted(SCHEMAS.keys()):
        print_schema_info(data_type, truncate_names)


def create_schema_file(output_dir, truncate_names=True):
    """
    Create a comprehensive schema definition file for all data types.
    
    Args:
        output_dir: Directory where extract files are stored
        truncate_names: Boolean to control whether field names are truncated to fit field width
    
    Returns:
        bool: True if successful, False otherwise
    """
    schema_file_path = output_dir / "extract_schemas.txt"
    
    try:
        with open(schema_file_path, 'w') as f:
            # Write header
            f.write("Clinical Data Extract Schema Definitions\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Write schema for each data type
            for data_type in sorted(SCHEMAS.keys()):
                schema = SCHEMAS[data_type]
                
                # Write data type header
                f.write(f"{data_type} Schema Definition:\n")
                f.write("=" * 80 + "\n")
                f.write(f"{'Field Name':<21} | {'Len':<4} | {'Type':<5} | {'Just':<5} | {'Pad':<4} | {'Header Display'}\n")
                f.write("-" * 80 + "\n")
                
                # Write field definitions
                total_length = 0
                for field_def in schema:
                    # Check if field name exceeds the field length
                    field_name = field_def['name']
                    field_length = field_def['length']
                    
                    # Optionally truncate header display if field name is too long
                    if truncate_names and len(field_name) > field_length:
                        header_display = field_name[:field_length]
                    else:
                        header_display = field_name
                        
                    f.write(f"{field_def['name']:<21} | {field_def['length']:<4} | {field_def['data_type']:<5} | {field_def['justify']:<5} | '{field_def['pad_char']}'  | '{header_display}'\n")
                    total_length += field_def['length']
                
                f.write("-" * 80 + "\n")
                f.write(f"Total record length: {total_length} characters\n\n")
            
            # Write summary
            f.write("Summary:\n")
            f.write("=" * 40 + "\n")
            f.write(f"Total Data Types: {len(SCHEMAS)} ({', '.join(sorted(SCHEMAS.keys()))})\n")
            f.write(f"Total Extract Files Generated: {len(SCHEMAS)}\n")
            f.write(f"Output Directory: {output_dir}\n")
            f.write(f"Schema File: {schema_file_path.name}\n")
            
        print(f"✓ Schema definitions saved to '{schema_file_path.name}'")
        return True
        
    except Exception as e:
        print(f"Error creating schema file '{schema_file_path.name}': {e}")
        return False


def main():
    """Main execution function."""
    # Parse command line arguments using argparse module
    parser = argparse.ArgumentParser(
        description='Generate clinical data extract files with optional header truncation'
    )
    parser.add_argument('-t', '--truncate', action='store_true',
                       help='Truncate header field names to match field lengths (default: False)')
    args = parser.parse_args()
    truncate_headers = args.truncate
    
    print(f"\n\033[34mClinical Data Extract Generator\033[0m\n")
    if truncate_headers:
        print("\033[33mHeader Truncation: ENABLED\033[0m (field names are truncated to fit column widths)")
    else:
        print("\033[33mHeader Truncation: DISABLED\033[0m (full field names are used in headers)")
    print("=" * 80)
    print("This program creates sample ASCII fixed-length extract files")
    print("for mainframe/SAS systems with the following data types:")
    
    for data_type in sorted(SCHEMAS.keys()):
        if data_type == 'ADM':
            desc = "Admissions"
        elif data_type == 'CLI':
            desc = "Clinic"
        elif data_type == 'DEM':
            desc = "Demographics"
        elif data_type == 'LAB':
            desc = "Laboratory"
        elif data_type == 'MOV':
            desc = "Physical Movement"
        else:
            desc = "Unknown data type"
        print(f"- {data_type}: {desc}")
    
    print("=" * 80)
    print()
    
    # Display all available schemas
    print_all_schemas(truncate_headers)
    
    # Create timestamped output directory
    output_dir = create_output_directory()
    print(f"Creating extract files in directory: {output_dir}")
    print()
    
    # Create schema definition file
    print("Creating schema definition file...")
    create_schema_file(output_dir, truncate_headers)
    print()
    
    # Create sample files for each data type
    data_types = sorted(SCHEMAS.keys())
    success_count = 0
    
    for data_type in data_types:
        filename = f"{data_type.lower()}_extract.txt"
        print(f"\n{'='* 60}")
        print(f"Creating {data_type} extract file...")
        print(f"{'='* 60}")
        
        if create_sample_extract_file(data_type, filename, DEFAULT_RECORDS_PER_FILE, output_dir, truncate_headers):
            success_count += 1
        else:
            print(f"✗ Failed to create {data_type} extract file!")
    
    # Final summary
    print(f"\n{'='* 60}")
    print(f"Extract Generation Complete!")
    print(f"{'='* 60}")
    print(f"Files created: {success_count}/{len(data_types)}")
    print(f"Output directory: {output_dir}")
    
    if success_count == len(data_types):
        print("✓ All files created successfully!")
        print("\nFiles created:")
        for data_type in data_types:
            filename = f"{data_type.lower()}_extract.txt"
            file_path = output_dir / filename
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"  - {filename} ({file_size} bytes)")
    else:
        print("✗ Some files failed to create. Check error messages above.")
    
    print(f"\n{'='* 60}")
    print("USAGE EXAMPLES:")
    print("---------------")
    print("# Import and use specific functions:")
    print("from create_sample_extract import create_sample_extract_file")
    print("create_sample_extract_file('ADM', 'my_data.txt', 50)")
    print()
    print("# View schema information:")
    print("from create_sample_extract import print_schema_info")
    print("print_schema_info('RAD')")
    print(f"{'='* 60}")


# Main execution block
if __name__ == "__main__":
    main()