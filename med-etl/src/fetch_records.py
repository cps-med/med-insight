# -----------------------------------------------------------------------
# fetch_records.py
# -----------------------------------------------------------------------
# Custom queries to get DSS extract data for each extract type
#  - ADM, LAB, RAD, CLI, MED (to be developed)
# -----------------------------------------------------------------------

# import required dependencies
from src.constants_general import *
from src.constants_sql_adm import *
from src.constants_sql_cli import *
from src.constants_sql_lbb import *
from src.constants_sql_rad import *
from src.db_config import create_connection, close_connection
from datetime import datetime
from src.minio_config import get_minio_s3_options, build_s3_path
import pyodbc
import pandas as pd
import os
from src.logging_config import get_logger

logger = get_logger(__name__)

# -----------------------------------------------------------
# Fetch ADM records
# -----------------------------------------------------------
def fetch_adm_records(station, start_date, end_date, extract_status):
    """Run querys to fetch records from tables in the CDWWork database and insert into Extract database."""

    # set function return code default value as true
    rc = True

    # create connection to CDWWork database
    connection_source_db = create_connection("CDWWork")
    if connection_source_db is None:
        rc = False
        return rc

    try:
        # create a cursor
        cursor_source_db = connection_source_db.cursor()

        # execute query 01
        print("Executing query to select Patient Cohort into global temp table")
        cursor_source_db.execute(ADM_QUERY_01, station, start_date, end_date)

        # execute query 02
        print("Executing query to select all rows from global temp table")
        cursor_source_db.execute(ADM_QUERY_02)

        # fetch all records from query 02 into a list
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} Records found\n")
            # Print each row with pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row), end="\n")
                print(RESET, end="")
        else:
            print("No records found from this select statement.")

        print()

        # execute query 03
        print("Executing query to select ADM extract dataset into global temp table")
        cursor_source_db.execute(ADM_QUERY_03)

        # execute query 04
        print("Executing query to select all rows from global temp table (unsorted)")
        cursor_source_db.execute(ADM_QUERY_04)

        # fetch all records (into list)
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} Records found\n")
            # Print each row with pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row), end="\n")
                print(RESET)
        else:
            print("No records found from this select statement.")

        print()

        # execute query 05
        print("Executing query to select all rows from global temp table (transformed & sorted)")
        cursor_source_db.execute(ADM_QUERY_05)

        # fetch all records (into list)
        records = cursor_source_db.fetchall()

        if records:
            print(f"{len(records)} Records found\n")
            # Print current VistA-based extract header
            print(f"{GREEN}{ADM_SEQUENCE_NUMBER}{ADM_YEAR_MONTH}{EXTRACT_NUMBER}{RESET}\n")
            # Print each row with pipe delimiter
            for row in records:
                print(GREEN + "|".join(str(value) for value in row), end="\n")
                print(RESET)

            # insert all records into Extract database 
            print("\nInserting records into Extract database...\n")

            # create connection to Extract database
            connection_target_db = create_connection("Extract")
            if connection_target_db is None:
                rc = False
                return rc
            else:
                print("\nConnection to target database successful...")

            try:
                # create a cursor
                cursor_target_db = connection_target_db.cursor()

                # prepare INSERT statement for Data.ADM table
                # excluding QueryTimestamp (has default) and QueryUser (can be NULL)
                insert_query = ADM_INSERT_01

                # prepare metadata variables to be inserted to record
                query_user = os.environ.get('USER', 'ETL_Process') # get current user or default
                extract_name = ADM_EXTRACT_NAME
                extract_version = ADM_EXTRACT_VERSION

                print(f"\nquery_user: {query_user}")
                print(f"\nextract_status: {extract_status}\n")

                # convert records to list of tuples and add metadata values
                record_tuples = []
                for record in records:
                    # convert record to list, add metadata values, then convert to tuple
                    record_list = list(record)
                    record_list.append(start_date)       # add RunStartDate to end of record
                    record_list.append(end_date)         # add RunEndDate to end of record
                    record_list.append(station)          # add RunSta3n to end of record
                    record_list.append(extract_name)     # add ExtractName to end of record
                    record_list.append(extract_version)  # add ExtractVersion to end of record
                    record_list.append(extract_status)   # add ExtractStatus at the end
                    record_list.append(datetime.now())   # add QueryTimestamp at the end
                    record_list.append(query_user)       # add QueryUser at the end
                    record_tuples.append(tuple(record_list))

                # execute bulk insert
                cursor_target_db.executemany(insert_query, record_tuples)
                connection_target_db.commit()

                print(f"Successfully inserted {len(records)} records into Data.ADM table\n")
                logger.info("Successfully processed %d ADM records for station %s (%s)", len(records), station, query_user)

            except pyodbc.Error as e:
                print(f"Database insert error: {e}")
                rc = False
                if connection_target_db:
                    connection_target_db.rollback()

            finally:
                if connection_target_db:
                    cursor_target_db.close()
                    close_connection(connection_target_db, "Extract")
        else:
            print("No records found from this select statement.")

        print()

    except pyodbc.Error as e:
        print(f"Error fetching records: {e}")
        rc = False

    finally:
        cursor_source_db.close()
        close_connection(connection_source_db, "CDWWork")

    return rc


# -----------------------------------------------------------
# Fetch LBB records
# -----------------------------------------------------------
def fetch_lbb_records(station, start_date, end_date, extract_status):
    """
    Fetch lab blood bank data from Parquet file stored in MinIO (S3-compatible).
    Print and insert into Extract DB (Data.LBB)
    """

    # set function return code default value as true
    rc = True

    # Build S3 path and get MinIO connection options
    parquet_s3_path = build_s3_path("extract-file/lbb/" + LBB_PARQUET_FILENAME)
    s3_options = get_minio_s3_options()

    try:
        # load Parquet file
        df = pd.read_parquet(parquet_s3_path, storage_options=s3_options)
        if not df.empty:
            print(f"{len(df)} Records found\n")
            for _, row in df.iterrows():
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            print()

            # connect to target DB
            connection_target_db = create_connection("Extract")
            if connection_target_db is None:
                rc = False
                return rc
            
            print("\nConnection to target database successful...")

            # prepare insert statement and metadata
            insert_query = LBB_INSERT_01
            extract_name = LBB_EXTRACT_NAME
            extract_version = LBB_EXTRACT_VERSION
            query_user = os.environ.get("USER", "ETL_Process")

            print(f"\nquery_user: {query_user}")
            print(f"extract_status: {extract_status}")

            try:
                cursor = connection_target_db.cursor()

                # convert DataFrame to list of tuples and add metadata
                record_tuples = []
                for _, row in df.iterrows():
                    # convert NaN values to None for SQL Server compatibility
                    # (thanks, claude code for debugging this tricky bug)
                    record_list = [None if pd.isna(val) else val for val in row.values]
                    record_list.append(start_date)
                    record_list.append(end_date)
                    record_list.append(station)
                    record_list.append(extract_name)
                    record_list.append(extract_version)
                    record_list.append(extract_status)
                    record_list.append(datetime.now())   # add QueryTimestamp at the end
                    record_list.append(query_user)
                    record_tuples.append(tuple(record_list))

                # bulk insert
                cursor.executemany(insert_query, record_tuples)
                connection_target_db.commit()

                print(f"Successfully inserted {len(record_tuples)} records into Data.LBB table\n")
                logger.info("Successfully processed %d LBB records for station %s (%s)", len(record_tuples), station, query_user)

            except pyodbc.Error as e:
                print(f"Database insert error: {e}")
                rc = False
                if connection_target_db:
                    connection_target_db.rollback()
            finally:
                if connection_target_db:
                    cursor.close()
                    close_connection(connection_target_db, "Extract")
        else:
            print("No records found in Parquet file.")
            rc = False
        return rc

    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        rc = False
        return rc

# -----------------------------------------------------------
# Fetch RAD records
# -----------------------------------------------------------
def fetch_rad_records(station, start_date, end_date, extract_status):
    """
    Fetch radiation data from Parquet file stored in MinIO (S3-compatible).
    Print and insert into Extract DB (Data.RAD)
    """

    # set function return code default value as true
    rc = True

    # Build S3 path and get MinIO connection options
    parquet_s3_path = build_s3_path("extract-file/rad/" + RAD_PARQUET_FILENAME)
    s3_options = get_minio_s3_options()

    try:
        # load Parquet file
        df = pd.read_parquet(parquet_s3_path, storage_options=s3_options)
        if not df.empty:
            print(f"{len(df)} Records found\n")
            for _, row in df.iterrows():
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            print()

            # connect to target DB
            connection_target_db = create_connection("Extract")
            if connection_target_db is None:
                rc = False
                return rc
            
            print("\nConnection to target database successful...")

            # prepare insert statement and metadata
            insert_query = RAD_INSERT_01
            extract_name = RAD_EXTRACT_NAME
            extract_version = RAD_EXTRACT_VERSION
            query_user = os.environ.get("USER", "ETL_Process")

            print(f"\nquery_user: {query_user}")
            print(f"extract_status: {extract_status}")

            try:
                cursor = connection_target_db.cursor()

                # convert DataFrame to list of tuples and add metadata
                record_tuples = []
                for _, row in df.iterrows():
                    # convert NaN values to None for SQL Server compatibility
                    # (thanks, claude code for debugging this tricky bug)
                    record_list = [None if pd.isna(val) else val for val in row.values]
                    record_list.append(start_date)
                    record_list.append(end_date)
                    record_list.append(station)
                    record_list.append(extract_name)
                    record_list.append(extract_version)
                    record_list.append(extract_status)
                    record_list.append(datetime.now())   # add QueryTimestamp at the end
                    record_list.append(query_user)
                    record_tuples.append(tuple(record_list))

                # bulk insert
                cursor.executemany(insert_query, record_tuples)
                connection_target_db.commit()

                print(f"Successfully inserted {len(record_tuples)} records into Data.RAD table\n")
                logger.info("Successfully processed %d RAD records for station %s (%s)", len(record_tuples), station, query_user)

            except pyodbc.Error as e:
                print(f"Database insert error: {e}")
                rc = False
                if connection_target_db:
                    connection_target_db.rollback()
            finally:
                if connection_target_db:
                    cursor.close()
                    close_connection(connection_target_db, "Extract")
        else:
            print("No records found in Parquet file.")
            rc = False
        return rc

    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        rc = False
        return rc


# -----------------------------------------------------------
# Fetch CLI records
# -----------------------------------------------------------
def fetch_cli_records(station, start_date, end_date, extract_status):
    """
    Fetch clinic data from a set of Parquet files stored in MinIO.
    Print and insert into Extract DB (Data.CLI)
    """

    # set function return code default value as true
    rc = True

    # Build S3 path and get MinIO connection options
    parquet_s3_path = build_s3_path("extract-file/cli/" + CLI_PARQUET_FILENAME)
    s3_options = get_minio_s3_options()

    try:
        # load Parquet file
        df = pd.read_parquet(parquet_s3_path, storage_options=s3_options)
        if not df.empty:
            print(f"{len(df)} Records found\n")
            for _, row in df.iterrows():
                print(GREEN + "|".join(str(value) for value in row) + RESET)
            print()

            # connect to target DB
            connection_target_db = create_connection("Extract")
            if connection_target_db is None:
                rc = False
                return rc
            
            print("\nConnection to target database successful...")

            # prepare insert statement and metadata
            insert_query = CLI_INSERT_01
            extract_name = CLI_EXTRACT_NAME
            extract_version = CLI_EXTRACT_VERSION
            query_user = os.environ.get("USER", "ETL_Process")

            print(f"\nquery_user: {query_user}")
            print(f"extract_status: {extract_status}")

            try:
                cursor = connection_target_db.cursor()

                # convert DataFrame to list of tuples and add metadata
                record_tuples = []
                for _, row in df.iterrows():
                    # convert NaN values to None for SQL Server compatibility
                    # (thanks, claude code for debugging this tricky bug)
                    record_list = [None if pd.isna(val) else val for val in row.values]
                    record_list.append(start_date)
                    record_list.append(end_date)
                    record_list.append(station)
                    record_list.append(extract_name)
                    record_list.append(extract_version)
                    record_list.append(extract_status)
                    record_list.append(datetime.now())   # add QueryTimestamp at the end
                    record_list.append(query_user)
                    record_tuples.append(tuple(record_list))

                # bulk insert
                cursor.executemany(insert_query, record_tuples)
                connection_target_db.commit()

                print(f"Successfully inserted {len(record_tuples)} records into Data.CLI table\n")
                logger.info("Successfully processed %d CLI records for station %s (%s)", len(record_tuples), station, query_user)

            except pyodbc.Error as e:
                print(f"Database insert error: {e}")
                rc = False
                if connection_target_db:
                    connection_target_db.rollback()
            finally:
                if connection_target_db:
                    cursor.close()
                    close_connection(connection_target_db, "Extract")
        else:
            print("No records found in Parquet file.")
            rc = False
        return rc

    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        rc = False
        return rc
