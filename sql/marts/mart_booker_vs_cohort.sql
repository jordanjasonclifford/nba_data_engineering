 SELECT b.season,
    b.gp,
    b.ppg,
    e.cohort_ppg_avg,
    b.ppg - e.cohort_ppg_avg AS ppg_minus_cohort,
        CASE
            WHEN e.cohort_ppg_avg = 0::numeric THEN NULL::numeric
            ELSE b.ppg / e.cohort_ppg_avg
        END AS ppg_relative_index,
    b.apg,
    e.cohort_apg_avg,
    b.apg - e.cohort_apg_avg AS apg_minus_cohort,
    b.rpg,
    e.cohort_rpg_avg,
    b.rpg - e.cohort_rpg_avg AS rpg_minus_cohort,
    b.pts_std
   FROM mart_player_season b
     JOIN mart_allstar_environment e ON e.season = b.season
  WHERE b.player_name = 'Devin Booker'::text;
