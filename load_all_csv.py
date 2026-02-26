import os
import pandas as pd

def load_all_csvs(folder="data/csv"):
    csv_dict = {}

    for file in os.listdir(folder):
        if file.endswith('.csv'):
            path = os.path.join(folder, file)
            df = pd.read_csv(path)
            csv_dict[file] = df
        
    return csv_dict

if __name__ == "__main__":
    data = load_all_csvs()
    for name, df in data.items():
        print("\n===== ", name, " =====")
        print(df.head())