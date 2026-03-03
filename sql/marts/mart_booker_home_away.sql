CREATE OR REPLACE VIEW mart_booker_home_away AS
SELECT
  season,
  home_away,
  games,
  wins,
  losses,
  ppg,
  apg,
  rpg,
  fg_pct,
  fg3_pct,
  ft_pct
FROM mart_player_home_away
WHERE player_name = 'Devin Booker';