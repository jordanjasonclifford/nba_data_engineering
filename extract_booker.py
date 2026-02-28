from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time

# PLAYER ID
PLAYER_ID = ""
# BOOKER_ID = "1626164"

# Seasons Booker has played (string format required by API)
seasons = {
    "2015-16": "2015-16",
    "2016-17": "2016-17",
    "2017-18": "2017-18",
    "2018-19": "2018-19",
    "2019-20": "2019-20",
    "2020-21": "2020-21",
    "2021-22": "2021-22",
    "2022-23": "2022-23",
    "2023-24": "2023-24",
    "2024-25": "2024-25",
    "2025-26": "2025-26"
}

all_data = {}

for season_label, season in seasons.items():
    print(f"Pulling {season}...")
    
    gamelog = playergamelog.PlayerGameLog(
        player_id=PLAYER_ID,
        season=season
    )
    
    df = gamelog.get_data_frames()[0]
    
    df["SEASON"] = season_label  # Add season column
    all_data[season_label] = df
    
    time.sleep(0.6)  # Prevent rate limiting

# Combine all seasons into one DataFrame
combined_df = pd.concat(all_data.values(), ignore_index=True)

# Save to CSV
combined_df.to_csv("to_csvs/devin_booker_full_gamelogs_2015_2026.csv", index=False)

print("Done. CSV saved.")