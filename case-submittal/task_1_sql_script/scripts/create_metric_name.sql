CREATE OR REPLACE TABLE "RULA_CASE_STUDY"."PUBLIC"."METRIC_NAMES" AS
SELECT distinct metric_source
FROM rula_case_study.public.provider_monthly_metrics;