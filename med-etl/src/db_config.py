# -----------------------------------------------------------------------
# db_config.py
# -----------------------------------------------------------------------

import pyodbc
from dotenv import load_dotenv
import os

# load environment variables from the .env file
load_dotenv()

def create_connection(db_name):
    """
    Creates and returns a connection to designated SQL Server database. The
    two 'Trust' related string literal parameters are specific to either macOS
    or Windows, so depending on your envirionment, one can be commented out.
    """
    db_key = db_name.upper();
    print(f"Creating new connection with prefix: {db_key}")

    driver = os.getenv(f"{db_key}_DB_DRIVER")
    server = os.getenv(f"{db_key}_DB_SERVER")
    database = os.getenv(f"{db_key}_DB_NAME")
    username = os.getenv(f"{db_key}_DB_USER")
    password = os.getenv(f"{db_key}_DB_PASSWORD")
    trusted_connection = os.getenv(f"TRUST_CONNECTION")
    trust_certificate = os.getenv(f"TRUST_CERT")

    # validates that all required environment variables are present and == None
    if not all([driver, server, database, username, password, trusted_connection, trust_certificate]):
        raise ValueError(f"Missing environment variables for database: {db_name}")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        #f"Trusted_Connection={trusted_connection};"
        f"TrustServerCertificate={trust_certificate};"
    )

    try:
        connection = pyodbc.connect(connection_string)
        print(f"Connected to {db_name} successfully.")
        return connection
    
    except pyodbc.Error as e:
        print(f"Error while connecting to SQL Server: {e}")
        return None

def close_connection(connection, db_name=""):
    """Close the given database connection."""
    try:
        connection.close()
        print(f"SQL Server connection for {db_name} is closed")
    except pyodbc.Error as e:
        print(f"Error while closing connection for {db_name}: {e}")
