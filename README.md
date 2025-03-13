# Operations Insights Manager | Case 

## Overview

This repository contains the analysis and findings from a case study provided as part of Operations Insights Manager interview process.  The objective of this study is to demonstrate competencies in:

* SQL to perform EDA as directed
* Python by creating data transformation and export script
* Data analysis and critical thinking

The [raw data](data/Rula%20Insights%20Manager%20Case%20Data.xlsx) is provided as excel file, and can be found in /data directory.


## Navigation and Content

This repository is organized as follows:

* **`case/`**:
    * Contains instructions, walkthrough, and deliverables for each tasks
    * [task_1_sql_script](case/task_1_sql_script/README.md)
    * [task_2_export_script](case/task_2_export_script/README.md)
    * [task_3_insights_and_rec](case/task_3_insights_and_rec/README.md)
* **`data/`**:
    * Contains the raw and processed datasets used in the analysis.
    * [Raw data](data/Rula%20Insights%20Manager%20Case%20Data.xlsx)
    * [Cleaned Data](data/case_data_cleaned.pkl)
    * [Summary for Each Metrics](data/case_data_target_miss_streak.pkl)
    * [Summary for Each Providers](data/case_data_performance_miss_streak.pkl)
    * [Data report for Proviers](data/provider_export_report/)
* **`docs/`**:
    * Contains standalone Jupyternotebook walking through functions and scripts used in deliverables
    * [Data Quality Check](docs/01_data_quality_check.ipynb)
    * [Data Cleaning](docs/02_data_cleaning.ipynb)
    * [Data Transofrmation](docs/03_data_transformation.ipynb)
    * [Visualization](docs/04_visualize.ipynb)
    * [Long to Wide Table](docs/05_tidy_to_wide_table.ipynb)
    * [Export using Google Sheet API](docs/06_saving_to_gsheet.ipynb)
    * [Additional Exploration](docs/07_other_metrics.ipynb)
* **`requirements.txt`**:
    * Lists the Python packages required to run the code.
* **`README.md`**:
    * The current file, providing an overview of the repository.
