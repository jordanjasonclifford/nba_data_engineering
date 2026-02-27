from nba_api.stats.endpoints import playercareerstats

# Devin Booker
career = playercareerstats.PlayerCareerStats(player_id='1626164')

df = career.season_totals_regular_season.get_data_frame()

print(df[['SEASON_ID', 'TEAM_ABBREVIATION', 'PTS']])