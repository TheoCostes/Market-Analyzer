import os
import pandas as pd

os.chdir("..")


def create_global_dataset(path, min_days=150):

    df_global = pd.DataFrame()

    for file in os.listdir(path):
        if file.split(".")[1] != "csv":
            continue
        print("=======================================")
        print(file)
        df = pd.read_csv(path + file)
        df["token"] = file.split(".")[0]
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if len(df) > min_days:
                print(f"We have more than 6 months of data for {file.split('.')[0]}")
                df_global = pd.concat([df_global, df])
    df_global.to_csv(f"./data/df_global_{path.split('/')[-2]}.csv", index=False)
    return df_global


def compute_change(df):
    print(df.head())
    df["change_24h"] = df.groupby("token")["close"].pct_change(periods=1).values
    df["change_7d"] = df.groupby("token")["close"].pct_change(periods=7).values
    return df


df_global = create_global_dataset("./data/1d/")
print("=======================================")
print("DF GLOBAL created")
df_global = compute_change(df_global)
print(df_global.head())

# create a function that compute for each token the change in price over the last 24h and over the last 7 days
# and add it to the dataframe
