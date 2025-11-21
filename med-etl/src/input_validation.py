# -----------------------------------------------------------------------
# input_validation.py
# -----------------------------------------------------------------------
# Input validation functions for med-etl application.
# Provides validation for user inputs in main.py.
# Also prompts user to confirm values or cancel.
# -----------------------------------------------------------------------

from datetime import datetime, timedelta
import os
from src.constants_general import RED, YELLOW, GREEN, RESET


def validate_etl_function(function):
    """Validate ETL function against allowed values"""
    allowed_functions = ['1', '2']
    return str(function).strip() in allowed_functions


def validate_station_number(station):
    """Validate station number against allowed values"""
    allowed_stations = ['508', '516', '442', '552']
    return str(station).strip() in allowed_stations


def validate_date_format(date_string):
    """Parse and validate YYYY-MM-DD format"""
    try:
        datetime.strptime(date_string.strip(), '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_date_range(start_date, end_date):
    """Validate logical date relationships"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        # End date must be after start date
        if end <= start:
            return False
            
        # Reasonable range check (not more than 1 year)
        if (end - start).days > 365:
            return False
            
        # Not future dates beyond today
        if end > datetime.now():
            return False
            
        return True
    except ValueError:
        return False


def validate_extract_type(extract):
    """Check against allowed extract types"""
    allowed_types = ['ADM', 'LBB', 'RAD', 'CLI']
    return extract.upper().strip() in allowed_types


def validate_extract_status(status):
    """Check against allowed status values"""
    allowed_statuses = ['audit', 'final']
    return status.lower().strip() in allowed_statuses


def sanitize_input(value):
    """Strip whitespace and normalize input"""
    return value.strip() if value else ""


def get_validated_input(prompt, validation_func, error_message, transform_func=None):
    """Generic input collection with validation retry logic"""
    while True:
        value = input(prompt).strip()
        
        if not value:
            print(f"{RED}Input cannot be empty. Please try again.{RESET}")
            continue
            
        # Apply transformation if provided (e.g., .upper(), .lower())
        if transform_func:
            value = transform_func(value)
            
        if validation_func(value):
            return value
        print(f"{RED}{error_message}{RESET}")


def get_etl_function():
    """Get, validate, and return user input for ETL function."""
    return get_validated_input(
        f"{YELLOW}    ETL Function (1-Get Data, 2-Create File): {RESET}",
        validate_etl_function,
        "Invalid ETL Function. Please enter 1 or 2."
    )


def get_station_number():
    """Collect and validate station number"""
    return get_validated_input(
        f"{YELLOW}       VistA Station (508, 516, 442, or 552): {RESET}",
        validate_station_number,
        "Invalid station number. Please enter 508, 516, 442, or 552."
    )


def get_extract_type():
    """Collect and validate extract type"""
    return get_validated_input(
        f"{YELLOW}           Extract Name (ADM, LBB, RAD, CLI): {RESET}",
        validate_extract_type,
        "Invalid extract type. Please enter ADM, LBB, RAD, or CLI.",
        str.upper
    )


def get_date_range():
    """Collect and validate date range"""
    while True:
        start_date = get_validated_input(
            f"{YELLOW}                     Start Date (YYYY-MM-DD): {RESET}",
            validate_date_format,
            "Invalid date format. Please use YYYY-MM-DD (e.g., 2025-01-15)."
        )
        
        end_date = get_validated_input(
            f"{YELLOW}                       End Date (YYYY-MM-DD): {RESET}",
            validate_date_format,
            "Invalid date format. Please use YYYY-MM-DD (e.g., 2025-01-15)."
        )
        
        if validate_date_range(start_date, end_date):
            return start_date, end_date
        
        print(f"{RED}Invalid date range. End date must be after start date, "
              f"within 1 year, and not in the future.{RESET}")


def get_extract_status():
    """Collect and validate extract status"""
    return get_validated_input(
        f"{YELLOW}             Extract Status (audit or final): {RESET}",
        validate_extract_status,
        "Invalid extract status. Please enter 'audit' or 'final'.",
        str.lower
    )

def print_input_summary(function, station, extract, start_date, end_date, extract_status):
    """Display input summary for user confirmation in a formatted box"""
    print()
    print(f"{YELLOW}╔═══════════════════════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}║                   INPUT SUMMARY                       ║{RESET}")
    print(f"{YELLOW}╠═══════════════════════════════════════════════════════╣{RESET}")
    print(f"{YELLOW}║{RESET}  ETL Function:       {GREEN}{function:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}║{RESET}  Station Number:     {GREEN}{station:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}║{RESET}  Extract Type:       {GREEN}{extract:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}║{RESET}  Start Date:         {GREEN}{start_date:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}║{RESET}  End Date:           {GREEN}{end_date:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}║{RESET}  Extract Status:     {GREEN}{extract_status:30s}{RESET} {YELLOW}  ║{RESET}")
    print(f"{YELLOW}╚═══════════════════════════════════════════════════════╝{RESET}")
    print()


def get_user_confirmation():
    """Prompt user to continue or cancel after reviewing input summary"""
    return get_validated_input(
        f"{YELLOW}Continue with this configuration? (y/n): {RESET}",
        lambda x: x.lower() in ['y', 'yes', 'n', 'no'],
        "Please enter 'y' for yes or 'n' for no.",
        str.lower
    )
