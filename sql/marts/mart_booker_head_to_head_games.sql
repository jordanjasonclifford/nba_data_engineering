 SELECT b.game_id,
    b.game_date,
    b.season,
    o.player_name AS opponent,
        CASE
            WHEN split_part(b.matchup, ' '::text, 1) = split_part(o.matchup, ' '::text, 1) THEN 'WITH'::text
            ELSE 'AGAINST'::text
        END AS context,
    b.pts AS booker_pts,
    b.ast AS booker_ast,
    b.reb AS booker_reb,
    b.fgm AS booker_fgm,
    b.fga AS booker_fga,
    b.fg3m AS booker_fg3m,
    b.fg3a AS booker_fg3a,
    b.ftm AS booker_ftm,
    b.fta AS booker_fta,
    b.wl AS booker_result,
    o.pts AS opp_pts,
    o.ast AS opp_ast,
    o.reb AS opp_reb,
    o.fgm AS opp_fgm,
    o.fga AS opp_fga,
    o.fg3m AS opp_fg3m,
    o.fg3a AS opp_fg3a,
    o.ftm AS opp_ftm,
    o.fta AS opp_fta
   FROM fact_player_game b
     JOIN fact_player_game o ON b.game_id = o.game_id AND b.player_name <> o.player_name
     JOIN dim_allstar_cohort c ON c.player_name = o.player_name
  WHERE b.player_name = 'Devin Booker'::text;
