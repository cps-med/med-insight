# -----------------------------------------------------------------------
# create_extracts.py
# -----------------------------------------------------------------------
# Generate fixed-width ASCII extract files from Extract database tables
# -----------------------------------------------------------------------

# import required dependencies
from src.constants_general import *
from src.constants_ascii_adm import *
# from src.constants_ascii_lbb import *
# from src.constants_ascii_rad import *

from src.db_config import create_connection, close_connection
from datetime import datetime
from src.minio_config import get_minio_s3_options, build_s3_path
import pyodbc
import pandas as pd
import os
from src.logging_config import get_logger

logger = get_logger(__name__)
extract_user = os.environ.get("USER", "ETL_Process")

# -----------------------------------------------------------
# Helper Function
# -----------------------------------------------------------
def format_extract_row(row_data, field_specs):
    """Format a single extract record according to field specifications"""
    formatted_fields = []
    for i, (field_name, width, alignment, padding_char) in enumerate(field_specs):
        value = str(row_data[i]) if row_data[i] is not None else ""
        if alignment == "left":
            formatted_field = value.ljust(width, padding_char)[:width]
        else:
            formatted_field = value.rjust(width, padding_char)[:width]
        formatted_fields.append(formatted_field)
    return "".join(formatted_fields)


# -----------------------------------------------------------
# Create ADM Extract
# -----------------------------------------------------------
def create_adm_extract(station, start_date, end_date, extract_status):
    """Query Extract.Data.ADM and create fixed-width ASCII file"""

    # set function return code with default value as true
    rc = True

    # create connection to Extract database
    connection_source_db = create_connection("Extract")
    if connection_source_db is None:
        rc = False
        return rc

    try:
        # create a cursor
        cursor_source_db = connection_source_db.cursor()

        # execute query 01
        print("Executing SELECT query to get rows per filter criteria")
        cursor_source_db.execute(ADM_QUERY_01, station, start_date, end_date, extract_status)

        # fetch all records from query 01 into a list
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} records found \n")
            # Print each row with a pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            
            # Generate ASCII extract file
            try:
                # Get output directory and expand ~ for home directory
                ascii_folder = os.path.expanduser(os.getenv("ASCII_EXTRACT_FOLDER", "./extract/"))
                
                # Create directory if it doesn't exist
                os.makedirs(ascii_folder, exist_ok=True)
                
                # Generate filename
                start_date_str = start_date.replace("-", "")[2:]  # Convert YYYYMMDD to YYMMDD
                end_date_str = end_date.replace("-", "")[2:]      # Convert YYYYMMDD to YYMMDD
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"adm_ext_{station}_{start_date_str}_{end_date_str}_{extract_status}_{timestamp}.txt"
                filepath = os.path.join(ascii_folder, filename)
                
                # Write ASCII file
                with open(filepath, 'w') as f:
                    # Write header row
                    f.write(ADM_HEADER_ROW + '\n')
                    
                    # Write formatted data rows
                    for row in records:
                        formatted_row = format_extract_row(row, ADM_FIELD_SPECS)
                        f.write(formatted_row + '\n')
                
                print(f"ASCII extract file created: {filepath}")
                print(f"File contains {len(records)} data records plus header row")
                logger.info("Created ADM extract file: %s (%d records) (%s)", filename, len(records), extract_user)
                
            except Exception as e:
                print(f"Error creating ASCII file: {e}")
                rc = False
        else:
            print("No records found from this select statement.\n")

    except pyodbc.Error as e:
        print(f"Error fetching records: {e}")
        rc = False

    finally:
        cursor_source_db.close()
        close_connection(connection_source_db, "Extract")

    return rc


# -----------------------------------------------------------
# Create LBB Extract
# -----------------------------------------------------------
def create_lbb_extract(station, start_date, end_date, extract_status):
    """Query Extract.Data.LBB and create fixed-width ASCII file"""

    # set function return code with default value as true
    rc = True

    # create connection to Extract database
    connection_source_db = create_connection("Extract")
    if connection_source_db is None:
        rc = False
        return rc

    try:
        # create a cursor
        cursor_source_db = connection_source_db.cursor()

        # execute query 01
        print("Executing SELECT query to get rows per filter criteria")
        cursor_source_db.execute(LBB_QUERY_01, station, start_date, end_date, extract_status)

        # fetch all records from query 01 into a list
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} records found \n")
            # Print each row with a pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            
            # Generate ASCII extract file
            try:
                # Get output directory and expand ~ for home directory
                ascii_folder = os.path.expanduser(os.getenv("ASCII_EXTRACT_FOLDER", "./extract/"))
                
                # Create directory if it doesn't exist
                os.makedirs(ascii_folder, exist_ok=True)
                
                # Generate filename
                start_date_str = start_date.replace("-", "")[2:]  # Convert YYYYMMDD to YYMMDD
                end_date_str = end_date.replace("-", "")[2:]      # Convert YYYYMMDD to YYMMDD
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"lbb_ext_{station}_{start_date_str}_{end_date_str}_{extract_status}_{timestamp}.txt"
                filepath = os.path.join(ascii_folder, filename)
                
                # Write ASCII file
                with open(filepath, 'w') as f:
                    # Write header row
                    f.write(LBB_HEADER_ROW + '\n')
                    
                    # Write formatted data rows
                    for row in records:
                        formatted_row = format_extract_row(row, LBB_FIELD_SPECS)
                        f.write(formatted_row + '\n')
                
                print(f"ASCII extract file created: {filepath}")
                print(f"File contains {len(records)} data records plus header row")
                logger.info("Created LBB extract file: %s (%d records) (%s)", filename, len(records), extract_user)

            except Exception as e:
                print(f"Error creating ASCII file: {e}")
                rc = False
        else:
            print("No records found from this select statement.\n")

    except pyodbc.Error as e:
        print(f"Error fetching records: {e}")
        rc = False

    finally:
        cursor_source_db.close()
        close_connection(connection_source_db, "Extract")

    return rc


# -----------------------------------------------------------
# Create RAD Extract
# -----------------------------------------------------------
def create_rad_extract(station, start_date, end_date, extract_status):
    """Query Extract.Data.RAD and create fixed-width ASCII file"""

    # set function return code with default value as true
    rc = True

    # create connection to Extract database
    connection_source_db = create_connection("Extract")
    if connection_source_db is None:
        rc = False
        return rc

    try:
        # create a cursor
        cursor_source_db = connection_source_db.cursor()

        # execute query 01
        print("Executing SELECT query to get rows per filter criteria")
        cursor_source_db.execute(RAD_QUERY_01, station, start_date, end_date, extract_status)

        # fetch all records from query 01 into a list
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} records found \n")
            # Print each row with a pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            
            # Generate ASCII extract file
            try:
                # Get output directory and expand ~ for home directory
                ascii_folder = os.path.expanduser(os.getenv("ASCII_EXTRACT_FOLDER", "./extract/"))
                
                # Create directory if it doesn't exist
                os.makedirs(ascii_folder, exist_ok=True)
                
                # Generate filename
                start_date_str = start_date.replace("-", "")[2:]  # Convert YYYYMMDD to YYMMDD
                end_date_str = end_date.replace("-", "")[2:]      # Convert YYYYMMDD to YYMMDD
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"rad_ext_{station}_{start_date_str}_{end_date_str}_{extract_status}_{timestamp}.txt"
                filepath = os.path.join(ascii_folder, filename)
                
                # Write ASCII file
                with open(filepath, 'w') as f:
                    # Write header row
                    f.write(RAD_HEADER_ROW + '\n')
                    
                    # Write formatted data rows
                    for row in records:
                        formatted_row = format_extract_row(row, RAD_FIELD_SPECS)
                        f.write(formatted_row + '\n')
                
                print(f"ASCII extract file created: {filepath}")
                print(f"File contains {len(records)} data records plus header row")
                logger.info("Created RAD extract file: %s (%d records) (%s)", filename, len(records), extract_user)
                
            except Exception as e:
                print(f"Error creating ASCII file: {e}")
                rc = False
        else:
            print("No records found from this select statement.\n")

    except pyodbc.Error as e:
        print(f"Error fetching records: {e}")
        rc = False

    finally:
        cursor_source_db.close()
        close_connection(connection_source_db, "Extract")

    return rc