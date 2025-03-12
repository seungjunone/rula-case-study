/* Jobs-to-do: Identify provider who made most improvement in MIC utilization rate
*/


-- Cleaning source data
WITH src_provider_metric as (
SELECT 
    replace(provider, 'Provider')::int as provider_id,
    to_date(month_year, 'YYYY-MM') as month_year,
    metric_score,
    metric_source
FROM RULA_CASE_STUDY.PUBLIC.PROVIDER_MONTHLY_METRICS),

-- Create date spine for each metric and provider_id
-- Date range is 2023-09 to 2024-08
src_date_spline as (
SELECT *
FROM RULA_CASE_STUDY.PUBLIC.MONTHLY_DATE_SPLINE
CROSS JOIN RULA_CASE_STUDY.PUBLIC.METRIC_NAMES
CROSS JOIN RULA_CASE_STUDY.PUBLIC.PROVIDER_IDS),

-- Join the source metric CTE to date spine
-- this CTE fills missing date ranges for all provider_id and metric_source.
missing_data_imputed as (
SELECT
    src_date_spline.provider_id as provider_id,
    src_date_spline.month_start as month_year,
    src_date_spline.metric_source as metric_source,
    metric_score as metric_score_original,
    nullifzero(src_provider_metric.metric_score) as metric_score
FROM src_date_spline
LEFT JOIN src_provider_metric
ON src_date_spline.month_start = src_provider_metric.month_year AND
   src_date_spline.metric_source = src_provider_metric.metric_source AND
   src_date_spline.provider_id = src_provider_metric.provider_id),

-- Keep only mic_utilization_rate_months metric.
-- Calculate initial and final mic_utilization_rate_months 
mic_util_initial_and_final_score as (
SELECT 
    provider_id,
    month_year,
    CASE WHEN row_number() OVER (partition by provider_id order by month_year asc) = 1
        THEN metric_score ELSE NULL END as initial_metric_score,
    CASE WHEN row_number() OVER (partition by provider_id order by month_year desc) = 1
        THEN metric_score ELSE NULL END as final_metric_score 
    
FROM missing_data_imputed
WHERE 
    metric_source = 'mic_utilization_rate_months' AND 
    metric_score IS NOT NULL
),

mic_util_summary as (

SELECT 
    provider_id, 
    min(month_year) as metric_initial_month_year,
    max(month_year) as metric_final_month_year,
    max(initial_metric_score) as initial_metric_score,
    max(final_metric_score) as final_metric_score
FROM mic_util_initial_and_final_score
GROUP BY provider_id
ORDER BY provider_id
)

SELECT 
    provider_id,
    metric_initial_month_year,
    metric_final_month_year,
    DATEDIFF('month', metric_initial_month_year, metric_final_month_year) as metric_months_observed,
    initial_metric_score,
    final_metric_score,
    final_metric_score - initial_metric_score as change_in_metric_score,
    change_in_metric_score / initial_metric_score * 100 as pct_change_in_metric_score,
    change_in_metric_score / nullifzero(metric_months_observed) as mic_improvement_monthly,
    dense_rank() OVER (ORDER BY change_in_metric_score desc) as mic_improvement_rank_overall_change,
    dense_rank() OVER (ORDER BY pct_change_in_metric_score desc) as mic_improvement_rank_pct_change,
    dense_rank() OVER (ORDER BY mic_improvement_monthly desc) as mic_improvement_rank_monthly_change
    
FROM 
    mic_util_summary
WHERE metric_months_observed > 0
ORDER BY mic_improvement_rank_overall_change