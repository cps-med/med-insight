# -----------------------------------------------------------------------
# main.py
# -----------------------------------------------------------------------
# Main application for initial interaction with the med-data SQL Server
# database that contains prepared ("Gold") data sourced from the VA
# Corporate Data Warehouse (CDW).
#
# The initial functionality is to read source data, perform additional
# transformations and data preparation, and present the output to
# screen in the form of a comma-separated value (CSV) text stream.
# -----------------------------------------------------------------------

# import required dependencies
from src.constants_general import *
from src.fetch_records import *
from src.create_extracts import *
from src.input_validation import *
import os

def main():
    """
    Prompt user for extract processing parameters, run fetch function for selected
    extract type, create extract, and update database with logging info (to-do).
    """
    print()
    print(f"{YELLOW}         +--------------------------------------------------+   {RESET}")
    print(f"{YELLOW}         |      Med-ETL - Data Preparation Pipeline         |   {RESET}")
    print(f"{YELLOW}         +--------------------------------------------------+   {RESET}")
    print()
        
    # Collect and validate inputs using validation functions
    etl_function = get_etl_function()
    station = get_station_number()
    extract = get_extract_type()
    start_date, end_date = get_date_range()
    extract_status = get_extract_status()
    
    # Display input summary for confirmation
    print_input_summary(etl_function, station, extract, start_date, end_date, extract_status)

    # Get user confirmation to proceed
    user_choice = get_user_confirmation()
    if user_choice in ['n', 'no']:
      print(f"{YELLOW}\nOperation cancelled by user.\n{RESET}")
      return

    print(f"{GREEN}\nProceeding with ETL processing...{RESET}")
    
    # initialize "return code" variable
    rc = None

    # Branch by ETL Function
    if etl_function == "1":
        print(f"{GREEN}Starting CDW/SDP data extraction...{RESET}")
        # fetch records for selected extract
        if extract == "ADM":
            rc = fetch_adm_records(station, start_date, end_date, extract_status)
        elif extract == "LBB":
            rc = fetch_lbb_records(station, start_date, end_date, extract_status)
        elif extract == "RAD":
            rc = fetch_rad_records(station, start_date, end_date, extract_status)
        elif extract == "CLI":
            rc = fetch_cli_records(station, start_date, end_date, extract_status)
        else:
            print(f"{RED}\nInvalid Extract Name: {extract}\n{RESET}")
            rc = False

        if rc:
            print(f"{BLUE}\nCDW data extraction and database load completed successfully.{RESET}")
        else:
            print("CDW data extraction and database load failed.")

    elif etl_function == "2":
        print(f"{GREEN}Starting ASCII extract file creation...{RESET}")
        # create extract files
        if extract == "ADM":
            rc = create_adm_extract(station, start_date, end_date, extract_status)
        elif extract == "LBB":
            rc = create_lbb_extract(station, start_date, end_date, extract_status)
        elif extract == "RAD":
            rc = create_rad_extract(station, start_date, end_date, extract_status)
        elif extract == "CLI":
            rc = create_cli_extract(station, start_date, end_date, extract_status)
        else:
            print(f"{RED}\nInvalid Extract Name: {extract}\n{RESET}")
            rc = False

        if rc:
            print(f"{BLUE}\nExtract file creation and save completed successfully.{RESET}")
        else:
            print(f"{RED}\nExtract file creation and save failed.{RESET}")

    else:
        print(f"{RED}\nInvalid ETL Function {etl_function}\n{RESET}")
        rc = False

    print("\nmain.py complete...\n")

if __name__ == "__main__":
    main()


