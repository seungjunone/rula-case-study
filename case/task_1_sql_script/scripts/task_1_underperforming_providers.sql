/* Jobs-to-do: Calculate monthly streak of missing performance target
   Missing 3 out of 5 metric target is considered missing performance target.
   Missing performance target for 3 consecutive month would label provider as underperforming.
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

-- Add metric target for each metric_source and determine if target was missed 
-- for given provider_id, month-year, and metric_source.
add_metric_target as (
SELECT 
    *,
    CASE 
        WHEN metric_source = 'average_responses_agg_month' THEN 4
        WHEN metric_source = 'caseloads_months' THEN 337
        WHEN metric_source = 'chart_review_months' THEN 0.80
        WHEN metric_source = 'documentation_rates_months' THEN 0.90
        WHEN metric_source = 'mic_utilization_rate_months' THEN 0.80
        ELSE -1 END as metric_target,
    CASE 
        WHEN metric_score < metric_target OR metric_score is NULL THEN 1 
        ELSE 0 END metric_target_missed
    
FROM missing_data_imputed
),

-- summarize per provider, month_year, how many metrics were missed
monthly_target_miss_summary as (
SELECT
    provider_id,
    month_year,
    sum(metric_target_missed) as num_metrics_missed

FROM add_metric_target
GROUP BY 1, 2
),

-- calculate if 3+ metrics were missed for a given provider_id and year-month
monthly_underperformance_flagged as (
SELECT 
    *,
    CASE WHEN num_metrics_missed >= 3 THEN 1 ELSE 0 END as monthly_performance_target_missed
FROM monthly_target_miss_summary
),

-- calculate the underperformance streak to show number of consecutive month
-- where 3+ metrics were missed for a given provider_id.
-- streak resets to 0 if provider meets the performance criteria.

monthly_underperformance_streak as (
    SELECT
        *,
        SUM(monthly_performance_target_missed) OVER (
            PARTITION BY provider_id, streak_group
            ORDER BY month_year
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS streak_underperformance
    FROM (
        SELECT
            *,
            SUM(CASE WHEN monthly_performance_target_missed = 0 THEN 1 ELSE 0 END) OVER (
                PARTITION BY provider_id
                ORDER BY month_year
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS streak_group
        FROM monthly_underperformance_flagged
    )
),

-- this and provider_exclusion CTE is used to exclude
-- any provider who had less than 3 months with metric reports.
provider_months_with_metrics as (
SELECT 
    provider_id,
    count(distinct month_year) as num_month_with_metrics
FROM src_provider_metric
GROUP BY 1
),

provider_exclusion as (
SELECT provider_id
FROM provider_months_with_metrics
WHERE num_month_with_metrics < 3
)

SELECT
    provider_id,
    month_year,
    num_metrics_missed,
    monthly_performance_target_missed,
    streak_underperformance
FROM monthly_underperformance_streak
WHERE 
    month_year = '2024-08-01' AND
    streak_underperformance >= 3 AND
    provider_id NOT IN (SELECT * FROM provider_exclusion)
ORDER BY 
    provider_id, month_year;