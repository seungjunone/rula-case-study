CREATE OR REPLACE TABLE "RULA_CASE_STUDY"."PUBLIC"."MONTHLY_DATE_SPLINE" AS

WITH RECURSIVE DateSeries AS (
    SELECT 
        '2023-09-01'::date AS month_start,
        '2024-08-01'::date AS max_month
    UNION ALL
    SELECT 
        ADD_MONTHS(month_start, 1),
        max_month
    FROM DateSeries
    WHERE month_start < max_month
)

SELECT month_start FROM DATESERIES;