SELECT
  season,
  gp,
  ppg,
  apg,
  rpg,
  mpg,
  pts_std,
  cohort_ppg_avg,
  ppg_minus_cohort,
  ppg_relative_index,
  cohort_apg_avg,
  apg_minus_cohort,
  cohort_rpg_avg,
  rpg_minus_cohort
FROM mart_player_vs_cohort
WHERE player_name = 'Devin Booker';