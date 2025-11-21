---------------------------------------------------------------------
-- Master SQL Script for Creating Extract Database
-- Run from terminal via zsh script:
-- ./_master.sh
---------------------------------------------------------------------

-- Drop and create database
:r db_database.sql

-- Create required schemas
:r db_schemas.sql

-- Create data tables
:r Data.ADM.sql
:r Data.LBB.sql
:r Data.RAD.sql
