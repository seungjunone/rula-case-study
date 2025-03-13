import pandas as pd
import numpy as np

def add_column_metric_target(df, metric_target_definition):
    """
    Adds a 'metric_target' column to a pandas DataFrame based on a dictionary.

    Args:
        df (pd.DataFrame): The input DataFrame.
        metric_target_definition (dict): A dictionary mapping 'metric_source' values to target scores.

    Returns:
        pd.DataFrame: The DataFrame with the added 'metric_target' column.
    """
    df['metric_target'] = df['metric_source'].map(metric_target_definition)
    return df

def add_column_has_met_target(df):
    """
    Adds a boolean 'as_met_target' column to a pandas DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame with 'metric_score' and 'metric_target' columns.

    Returns:
        pd.DataFrame: The DataFrame with the added 'as_met_target' column.
    """
    df['has_met_target'] = np.where(df['metric_score_imputed'].isnull(), np.nan, (df['metric_score_imputed'] >= df['metric_target']).astype(int))
    return df

def count_consecutive_misses_individual_metric(group):
    # Function to calculate consecutive misses
    count = 0
    for i in range(len(group)):
        if group.iloc[i]['has_met_target'] == 0:
            count += 1
        else:
            count = 0
        group.at[group.index[i], 'num_month_streak_metric_missed_target'] = count
    return group

def count_consecutive_misses_monthly_metric(group):
    # Function to calculate consecutive misses
    count = 0
    for i in range(len(group)):
        if group.iloc[i]['has_met_total_metric_count'] == 0:
            count += 1
        else:
            count = 0
        group.at[group.index[i], 'num_month_streak_metric_total_missed_target'] = count
    return group

def calculate_consecutive_misses(df, granularity, total_metric_count_threashold = 3):
    # Sort the dataframe by provider_id, metric_source, and month_year
    df = df.sort_values(by=['provider_id', 'metric_source', 'month_year'])
    
    if granularity == 'individual_metric':
        # Initialize a new column for counting consecutive misses
        df['num_month_streak_metric_missed_target'] = 0

        # Apply the function to each group
        df = df.groupby(['provider_id', 'metric_source'], group_keys=False)\
                .apply(count_consecutive_misses_individual_metric)
        
        # Reset index to ensure single index dataframe
        df = df.reset_index(drop=True)

    elif granularity == 'total_metrics_count':

        df = df.groupby(['provider_id', 'month_year'])\
            .agg(
                total_num_metric_target_met = ('has_met_target', 'sum'))\
            .reset_index()

        # Add the has_met_target_total_metric_count column
        df['has_met_total_metric_count'] = (
            df['total_num_metric_target_met'] >= total_metric_count_threashold
        ).astype(int)

        # Initialize a new column for counting consecutive misses
        df['num_month_streak_metric_total_missed_target'] = 0

        # Apply the function to each group
        df = df.groupby(['provider_id'], group_keys=False)\
                .apply(count_consecutive_misses_monthly_metric)

    return df

if __name__ == "__main__":
    print("calculate_metric.py can be imported as module")