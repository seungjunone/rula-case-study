CREATE OR REPLACE TABLE "RULA_CASE_STUDY"."PUBLIC"."PROVIDER_IDS" AS
SELECT distinct replace(provider, 'Provider')::int as provider_id
FROM rula_case_study.public.provider_monthly_metrics;