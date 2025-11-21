-----------------------------------------------------------------------------
-- Create: db_schemas.sql
-----------------------------------------------------------------------------
-- Schema owner: sa
-- List schemas: SELECT name AS SchemaName FROM sys.schemas ORDER BY name;
-----------------------------------------------------------------------------

USE Extract;
GO

-- create schema for extract tables
CREATE SCHEMA Data;
GO

-- create schema for metadata tables
CREATE SCHEMA Metadata;
GO
