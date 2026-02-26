import pandas as pd

def load_raw_data(): 
    """We are returning a read csv file"""
    return pd.read_csv("data/csv/other_stats.csv")

def pre_process(df):
    """Return a csv cleaned up when given a dataframe"""
    df['date'] = pd.to_datetime(df['date'])
    return df

def build_features(df):
    df['is_home'] = (df['location'] == 'Home').astype(int)

    return df