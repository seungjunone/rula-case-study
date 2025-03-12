## Objectives

This analysis aims to:

* Identify consistently underperforming providers (missing 3+ targets out of 5 over the last 3 months).
* Determine the top 5 providers with the greatest improvement in MIC utilization rate.


## Deliverables
| Task Summary | SQL File | SQL Output File | Note |
| --- | --- | --- | --- |
| Underperforming Providers | [task_1_underperforming_providers.sql](scripts/task_1_underperforming_providers.sql)



## Process Details

Before querying, a data quality check was conducted to ensure:

* Complete data for all 25 providers and 5 metrics.
* Unique records per provider, metric, and month.
* Continuous monthly data for all metrics and providers.

Detailed data quality checks are documented in [data_quality_check](docs/01_data_quality_check.ipynb). The data quality check flagged that some metrics do not have continuous monthly data, and the data needs to be modified to add rows for missing months. This step can be seen in [data_cleaning_and_transformation](docs/02_data_cleaning.ipynb).

Prior to constucting SQL queries, data transformation steps are tested as python script as documented in [data_transformation](docs/03_data_transformation.ipynb), which then were translated into SQL queries.

The raw data is uploaded to [personal snowflake instance](https://qsoynix-neb04412.snowflakecomputing.com/console/login#/), and SQL queries were constructed and executed in Snowflake's default UI (snowsight). 

1. The raw data is uploaded to `PUBLIC.RULA_CASE_STUDY.PUBLIC.PROVIDER_MONTHLY_METRICS`
1. Three dimensional tables are created to correct the missing date range issue:
    1. Date spline table is created using the [create_monthly_date_spline](scripts/create_monthly_date_spline.sql)
    1. Metrics name table is created using the [create_metric_name](scripts/create_metric_name.sql)
    1. Provider ID talbe is created using the [create_provider_id](scripts/create_provider_id.sql)
    1. Script to identify underperforming provider is created - [task_1_underperforming_providers.sql](scripts/task_1_underperforming_providers.sql). Its output is stored as [Task #1.1.csv](case-submittal/task_1_sql_script/output/Task #1.1.csv)
    2. Script to identify underperforming provider is created - [task_1_underperforming_providers.sql](scripts/task_1_underperforming_providers.sql). Its output is stored as [Task #1.2.csv](coutput/Task #1.2.csv)


## Results and Discussions

