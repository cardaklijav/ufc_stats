import pandas as pd
import numpy as np

fight_history_df = pd.read_csv("output/fighter_fight_history.csv")

def split_pair(value):
    if pd.isna(value):
        return None, None
    parts = str(value).split("  ")
    parts = [p.strip() for p in parts if p.strip() != ""]
    if len(parts) == 2:
        return parts[0], parts[1]
    return None, None


fighter_name_col = []
opponent_name_col = []
fighter_kd_col = []
opponent_kd_col = []
fighter_str_col = []
opponent_str_col = []
fighter_td_col = []
opponent_td_col = []
fighter_sub_col = []
opponent_sub_col = []

for _, row in fight_history_df.iterrows():
    f_name, o_name = split_pair(row["Fighter"])
    f_kd, o_kd = split_pair(row["Kd"])
    f_str, o_str = split_pair(row["Str"])
    f_td, o_td = split_pair(row["Td"])
    f_sub, o_sub = split_pair(row["Sub"])

    fighter_name_col.append(f_name)
    opponent_name_col.append(o_name)
    fighter_kd_col.append(f_kd)
    opponent_kd_col.append(o_kd)
    fighter_str_col.append(f_str)
    opponent_str_col.append(o_str)
    fighter_td_col.append(f_td)
    opponent_td_col.append(o_td)
    fighter_sub_col.append(f_sub)
    opponent_sub_col.append(o_sub)

fight_history_df["fighter_name"] = fighter_name_col
fight_history_df["opponent_name"] = opponent_name_col
fight_history_df["fighter_kd"] = fighter_kd_col
fight_history_df["opponent_kd"] = opponent_kd_col
fight_history_df["fighter_str"] = fighter_str_col
fight_history_df["opponent_str"] = opponent_str_col
fight_history_df["fighter_td"] = fighter_td_col
fight_history_df["opponent_td"] = opponent_td_col
fight_history_df["fighter_sub"] = fighter_sub_col
fight_history_df["opponent_sub"] = opponent_sub_col

stat_columns = ["fighter_kd", "opponent_kd", "fighter_str", "opponent_str",
                 "fighter_td", "opponent_td", "fighter_sub", "opponent_sub"]

for col in stat_columns:
    fight_history_df[col] = fight_history_df[col].replace("--", np.nan)

def make_match_key(row):
    names = tuple(sorted([str(row["fighter_name"]), str(row["opponent_name"])]))
    return f"{names[0]}|{names[1]}|{row['Event']}"

fight_history_df["match_key"] = fight_history_df.apply(make_match_key, axis=1)

key_counts = fight_history_df["match_key"].value_counts()
valid_keys = key_counts[key_counts >= 2].index

fight_history_df = fight_history_df[fight_history_df["match_key"].isin(valid_keys)]
fight_history_df = fight_history_df.drop_duplicates(subset="match_key", keep="first")

# importing fighters.csv to use the URL column
fighters_df = pd.read_csv("output/fighters.csv")

fighters_df["full_name"] = fighters_df["First"].fillna("") + " " + fighters_df["Last"].fillna("")
fighters_df["full_name"] = fighters_df["full_name"].str.strip()

name_to_url = dict(zip(fighters_df["full_name"], fighters_df["fighter_url"]))

fight_history_df["opponent_url"] = fight_history_df["opponent_name"].map(name_to_url)

# merging fighter career stats with fighter url
career_df = pd.read_csv("output/fighter_career_stats.csv")

fighter_career = career_df.add_prefix("fighter_")
fighter_career = fighter_career.rename(columns={"fighter_fighter_url": "fighter_url"})

opponent_career = career_df.add_prefix("opponent_")
opponent_career = opponent_career.rename(columns={"opponent_fighter_url": "opponent_url"})

merged_df = fight_history_df.merge(fighter_career, on="fighter_url", how="left")
merged_df = merged_df.merge(opponent_career, on="opponent_url", how="left")

# creating our target column
merged_df["fighter_won"] = (merged_df["W/L"] == "win").astype(int)
merged_df = merged_df[merged_df["W/L"].isin(["win", "loss"])]
columns_to_drop = ["fighter_url", "opponent_url", "match_key", "W/L", "Fighter"]
merged_df = merged_df.drop(columns=columns_to_drop, errors="ignore")

merged_df.to_csv("output/training_dataset.csv", index=False, encoding="utf-8-sig")
