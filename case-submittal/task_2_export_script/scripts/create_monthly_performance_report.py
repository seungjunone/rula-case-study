from datetime import datetime
import pandas as pd
import numpy as np
import warnings
import os
import clean_data
import calculate_metric
import transform_table_and_combine


# Load the source data
df_metric_score_by_provider_monthly = pd.read_excel("../../../data/Rula Insights Manager Case Data.xlsx")

# Clean Provider ID
df_metric_score_by_provider_monthly['Provider'] = df_metric_score_by_provider_monthly['Provider'].str.replace('Provider', '').astype(int)
df_metric_score_by_provider_monthly.rename(columns={'Provider': 'provider_id'}, inplace=True)

# Clean the input df and list for expand_date_range_with_metric_source function
df_metric_score_date_range = df_metric_score_by_provider_monthly\
    .groupby('provider_id')\
    .agg(min_month_year=('month_year', 'min'), max_month_year=('month_year', 'max'))\
    .reset_index()

metric_sources = df_metric_score_by_provider_monthly.metric_source.unique()

# Run `expand_date_range_with_metric_source` function
df_metric_score_date_range = clean_data.expand_date_range_with_metric_source(df_metric_score_date_range, metric_sources)

# join the output dataframe with original dataframe - df_metric_score_by_provider_monthly.
df_metric_score_by_provider_monthly_missing_date_filled = df_metric_score_date_range\
    .merge(
        df_metric_score_by_provider_monthly,
        how='left',
        on=['provider_id', 'month_year', 'metric_source'])\
    .sort_values(by=['provider_id', 'metric_source', 'month_year'], ascending=[True, True, True])\
    .reset_index(drop = True)

# Impute the missing data
df_metric_score_by_provider_zero_impute = clean_data.impute_missing_values(df_metric_score_by_provider_monthly_missing_date_filled, method = 'zero')

# define target metric
metric_target_definition = {
    "average_responses_agg_month": 4,
    "caseloads_months": 337,
    "chart_review_months": 0.80,
    "documentation_rates_months": 0.90, 
    "mic_utilization_rate_months": 0.80
}

# add metric target and met target flag
df_metric_score_by_provider_monthly_with_target = calculate_metric.add_column_metric_target(
    df = df_metric_score_by_provider_zero_impute,
    metric_target_definition = metric_target_definition)

df_metric_score_by_provider_monthly_with_target = calculate_metric.add_column_has_met_target(
    df = df_metric_score_by_provider_zero_impute)

df_metric_score_by_provider_monthly_with_target_sorted = df_metric_score_by_provider_monthly_with_target\
    .sort_values(by=['provider_id', 'metric_source', 'month_year'], ascending = [True, True, True])\
    .reset_index(drop=True)

# calculate metric target consecutive misses
df_metric_score_metric_target_miss_streak = calculate_metric.calculate_consecutive_misses(
    df_metric_score_by_provider_monthly_with_target_sorted, 'individual_metric')

# calculate metric total performance streak
df_metric_score_metric_underperformance_streak = calculate_metric.calculate_consecutive_misses(
    df_metric_score_by_provider_monthly_with_target_sorted, 'total_metrics_count', 3)

# convert wide to 
df_metric_score_metric_target_miss_streak_wide = transform_table_and_combine.compile_metric_target_info(df_metric_score_metric_target_miss_streak, 1)
df_metric_score_metric_underperformance_streak_wide = transform_table_and_combine.compile_metric_total_performance_info(df_metric_score_metric_underperformance_streak, 1)

df_provider_metric_and_performance_summary = pd.concat([df_metric_score_metric_target_miss_streak_wide, df_metric_score_metric_underperformance_streak_wide]).reset_index(drop = True)

provider_ids = df_metric_score_metric_target_miss_streak.provider_id.unique()

for provider_id in provider_ids:
    transform_table_and_combine.transform_and_save_provider_report(
        df_metric_score_metric_target_miss_streak,
        df_metric_score_metric_underperformance_streak,
        provider_id,
        "../output",
        "monthly_provider_report"
    )