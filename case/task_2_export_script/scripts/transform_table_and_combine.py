import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os

def compile_metric_target_info(df, provider):
    
    df = df[df["provider_id"] == provider]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore") 
        df['month_year'] = df['month_year'].dt.strftime('%Y-%m')

    df_pivot_metric = df\
        .pivot(index="metric_source", columns="month_year", values="metric_score_imputed")
    
    df_metric_miss_streak = df.copy()
    df_metric_miss_streak['metric_source'] = 'miss_streak__' + df_metric_miss_streak['metric_source'].astype(str)
    df_metric_miss_streak['metric_score_imputed'] = df_metric_miss_streak['metric_score_imputed'].astype(int)

    df_pivot_met_target = df_metric_miss_streak\
        .pivot(index="metric_source", columns="month_year", values="num_month_streak_metric_missed_target")

    df_concat = pd.concat([df_pivot_metric, df_pivot_met_target])

    df_concat.columns.name = None
    df_concat.reset_index(inplace=True)

    return df_concat

def compile_metric_total_performance_info(df, provider):
    
    df = df[df["provider_id"] == provider]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore") 
        df['month_year'] = df['month_year'].dt.strftime('%Y-%m')

    df_pivot_metric = df\
        .pivot(index="provider_id", columns="month_year", values="total_num_metric_target_met")\
        .reset_index(drop=True)
    df_pivot_metric['metric_source'] = "total_num_metric_target_met"


    df_pivot_met_target = df\
        .pivot(index="provider_id", columns="month_year", values="num_month_streak_metric_total_missed_target")\
        .reset_index(drop=True)
    df_pivot_met_target['metric_source'] = "num_month_streak_metric_total_missed_target"

    df_concat = pd.concat([df_pivot_metric, df_pivot_met_target])
    
    cols = ['metric_source'] + [col for col in df_concat.columns if col != 'metric_source']
    df_concat = df_concat[cols]

    df_concat.columns.name = None
    df_concat.reset_index(drop = True, inplace=True)

    return df_concat

def transform_and_save_provider_report(df_metric, df_performance, provider, export_path, export_filename):
    df_metric_score_metric_target_miss_streak_wide = compile_metric_target_info(df_metric, provider)
    df_metric_score_metric_underperformance_streak_wide = compile_metric_total_performance_info(df_performance, provider)
    df_provider_metric_and_performance_summary = pd.concat([df_metric_score_metric_target_miss_streak_wide, df_metric_score_metric_underperformance_streak_wide]).reset_index(drop = True)

    os.makedirs(export_path, exist_ok=True)

    today = datetime.today()
    year_month_stamp = today.strftime('%Y-%m')
    file_name = f"{export_filename}_{year_month_stamp}_provider_{provider}"
    df_provider_metric_and_performance_summary.to_csv(f'{export_path}/{file_name}.csv')  

    print(f"provider #{provider} report for {year_month_stamp} saved in '{export_path}/{file_name}.csv'")

if __name__ == "__main__":
    print("calculate_metric.py can be imported as module")