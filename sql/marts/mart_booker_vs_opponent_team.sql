SELECT
  season,
  opponent_team_abbr,
  games,
  wins,
  losses,
  ppg,
  apg,
  rpg,
  fg_pct,
  fg3_pct,
  ft_pct
FROM mart_player_vs_opponent_team
WHERE player_name = 'Devin Booker';