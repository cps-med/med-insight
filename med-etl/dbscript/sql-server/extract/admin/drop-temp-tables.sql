/*
|---------------------------------------------------------------
| Admin: Drop Temporary Tables
|---------------------------------------------------------------
*/

-- set the active database
USE CDWWork;
GO

-- drop global temporarytables
DROP TABLE IF EXISTS ##AdmPatientCohort;
DROP TABLE IF EXISTS ##AdmPatientExtract;
GO