import pandas as pd
import numpy as np

def expand_date_range_with_metric_source(df, metric_sources):
    """
    Expands the dataframe so that each row has a timestamp between min_month_year and max_month_year,
    and includes the metric_source for each provider.
    
    Parameters:
    df (pd.DataFrame): DataFrame with columns 'provider_id', 'min_month_year', and 'max_month_year'
    original_df (pd.DataFrame): Original DataFrame with columns 'provider_id', 'month_year', and 'metric_source'
    
    Returns:
    pd.DataFrame: Expanded DataFrame with each row having a timestamp between min_month_year and max_month_year,
                  and includes the metric_source for each provider
    """
    # Ensure the date columns are in datetime format
    df['min_month_year'] = pd.to_datetime(df['min_month_year'])
    df['max_month_year'] = pd.to_datetime(df['max_month_year'])
    
    # Create a list to hold the expanded rows
    expanded_rows = []
    
    # Iterate over each row in the dataframe
    for _, row in df.iterrows():
        # Generate a date range for each provider
        date_range = pd.date_range(start=row['min_month_year'], end=row['max_month_year'], freq='MS')
        for date in date_range:
            for metric_source in metric_sources:
                expanded_rows.append({'provider_id': row['provider_id'], 'month_year': date, 'metric_source': metric_source})
    
    # Create a new dataframe from the expanded rows
    expanded_df = pd.DataFrame(expanded_rows)
    
    return expanded_df

def impute_missing_values(df, method='median'):
    """
    Impute missing values in the DataFrame based on the specified method.
    
    Parameters:
    df (pd.DataFrame): DataFrame with missing values to be imputed.
    method (str): Method to impute missing values. Options are 'zero', 'median', 'average'.
    
    Returns:
    pd.DataFrame: DataFrame with missing values imputed.
    """

    if method not in ['zero', 'median', 'average']:
        raise ValueError("Method must be one of 'zero', 'median', or 'average'")    
    
    # Calculate median and mean metric scores
    agg_df = df.groupby(['provider_id', 'metric_source']).agg(
        median_metric_score=('metric_score', 'median'),
        mean_metric_score=('metric_score', 'mean')
    ).reset_index()

    # Merge the aggregated values back to the original dataframe
    df = df.merge(agg_df, on=['provider_id', 'metric_source'], how='left')

    df['zero_metric_score'] = 0    

    if method == 'zero':
        df['metric_score_imputed'] = df['metric_score'].combine_first(
            df['zero_metric_score']
        )        
    elif method == 'median':
        df['metric_score_imputed'] = df['metric_score'].combine_first(
            df['median_metric_score']
        ) 
    elif method == 'average':
        df['metric_score_imputed'] = df['metric_score'].combine_first(
            df['mean_metric_score']
        )
    
    # Add is_imputed column
    df['is_imputed'] = df['metric_score'].isna() & df['metric_score_imputed'].notna()
    
    # Drop unnecessary columns
    df = df.drop(columns=['zero_metric_score', 'mean_metric_score', 'median_metric_score'])
            
    return df

if __name__ == "__main__":
    print("clean_data.py can be imported as module")