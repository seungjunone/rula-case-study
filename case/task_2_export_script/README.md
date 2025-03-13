## Objectives

Write a script that can take data structured like this and generate a personalized Google sheet for each provider that can be shared with them on a monthly basis so they can understand their performance across each of these metrics through time against targets.

## Deliverables
The [create_monthly_performance_report.py](scripts/create_monthly_performance_report.py) script loads, cleans, transforms and export the provider level data to [output folder](output))

To execute the script, run the following command:
```
python create_monthly_performance_report.py
```

Here's a revised version, focusing on clarity, conciseness, and a more structured presentation:

Revised Description of Data Table Columns:

The script generates a data table containing columns categorized into three distinct groups:

* Monthly Metric Values:
    * `average_responses_agg_month`: Average responses aggregated for the month.
    * `caseloads_months`: Monthly caseloads.
    * `chart_review_months`: Monthly chart review rates.
    * `documentation_rates_months`: Monthly documentation rates.
    * `mic_utilization_rate_months`: Monthly MIC utilization rates.
* Metric Miss Streak (Consecutive Months Below Target):
    * `miss_streak__average_responses_agg_month`: Number of consecutive months where `average_responses_agg_month` was below the target.
    * `miss_streak__caseloads_months`: Number of consecutive months where `caseloads_months` was below the target.
    * `miss_streak__chart_review_months`: Number of consecutive months where `chart_review_months` was below the target.
    * `miss_streak__documentation_rates_months`: Number of consecutive months where `documentation_rates_months` was below the target.
    * `miss_streak__mic_utilization_rate_months`: Number of consecutive months where `mic_utilization_rate_months` was below the target.
* Overall Metric Performance:
    * `total_num_metric_target_met`: Total number of metrics meeting their respective targets for the month.
    * `num_month_streak_metric_total_missed_target`: Number of consecutive months where three or more metrics failed to meet their targets.

The script produces individual CSV reports for each provider, named according to the pattern: montly_provider_report_`{YEAR-MONTH of script run date}`_`{provider_id}`.csv. 

For instance, a report for provider 1 in March 2025 would be named 
```
monthly_provider_report_2025-03_provider_1.csv
```