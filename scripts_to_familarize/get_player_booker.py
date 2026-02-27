from nba_api.stats.endpoints import playergamelog

gamelog = playergamelog.PlayerGameLog(
    player_id='1626164',  # Booker
    season='2025-26'
)

df = gamelog.get_data_frames()[0]
print(df.head())