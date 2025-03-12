## Objectives

Write a script that can take data structured like this and generate a personalized
Google sheet for each provider that can be shared with them on a monthly basis
so they can understand their performance across each of these metrics through
time against targets

## Deliverables
The [create_monthly_performance_report.py](scripts/create_monthly_performance_report.py) script loads, cleans, transforms and export the provider level data to [output folder](/output))

Each file follows the following format.

`montly_provider_report`_`{YEAR-MONTH of script run date}`_`{provider_id}`.csv.

Example is: monthly_provider_report_2025-03_provider_1.csv


## Process Details

| Job to be done | Notebook for Demonstration |
| --- | --- | --- |
| Clean provider_id, address missing date range, and impute zero if metric is missing  | [02_data_cleaning.ipynb](../docs/02_data_cleaning.ipynb) | 
| Add target for each metric, and create target-met flag. Add metric target and metric count hit/miss and streaks for each month | [03_data_transformation.ipynb](../docs/03_data_transformation.ipynb) | 
| Pivot long table and combine metic target and metric count hit/miss into a single table | [05_tidy_to_wide_table.ipynb](../docs/05_tidy_to_wide_table.ipynb) | 

The outputs are store into [output](/output) folder as a separate file for each provider with following format:

`montly_provider_report`_`{YEAR-MONTH of script run date}`_`{provider_id}`.csv.

Example is: monthly_provider_report_2025-03_provider_1.csv





## Results and Discussions

### Identification of Underperforming Providers:
