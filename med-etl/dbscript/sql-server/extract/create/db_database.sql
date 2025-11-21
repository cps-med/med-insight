-----------------------------------------------------------------------
-- Create: db_database.sql
-----------------------------------------------------------------------

USE master;
GO

-- Check if database exists
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'Extract')
BEGIN
    PRINT '==> Extract exists. Terminating active connections...';
    -- Terminate connections and drop the database
    ALTER DATABASE Extract SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE Extract;
    PRINT '==> Extract database dropped.';
END
ELSE
BEGIN
    PRINT '==> Extract does not exist.';
END
GO

-- Create database
PRINT '==> Creating database Extract...';
CREATE DATABASE Extract;
GO

PRINT '==> Database Extract created successfully.';
GO
