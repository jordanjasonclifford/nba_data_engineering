 SELECT season,
    opponent,
    context,
    count(*) AS games,
    sum(
        CASE
            WHEN booker_result = 'W'::text THEN 1
            ELSE 0
        END) AS booker_wins,
    sum(
        CASE
            WHEN booker_result = 'L'::text THEN 1
            ELSE 0
        END) AS booker_losses,
    avg(booker_pts) AS booker_pts_pg,
    avg(booker_reb) AS booker_reb_pg,
    avg(booker_ast) AS booker_ast_pg,
        CASE
            WHEN sum(booker_fga) = 0::numeric THEN NULL::numeric
            ELSE sum(booker_fgm) * 1.0 / sum(booker_fga)
        END AS booker_fg_pct,
        CASE
            WHEN sum(booker_fg3a) = 0::numeric THEN NULL::numeric
            ELSE sum(booker_fg3m) * 1.0 / sum(booker_fg3a)
        END AS booker_fg3_pct,
        CASE
            WHEN sum(booker_fta) = 0::numeric THEN NULL::numeric
            ELSE sum(booker_ftm) * 1.0 / sum(booker_fta)
        END AS booker_ft_pct,
    avg(opp_pts) AS opp_pts_pg,
    avg(opp_reb) AS opp_reb_pg,
    avg(opp_ast) AS opp_ast_pg,
        CASE
            WHEN sum(opp_fga) = 0::numeric THEN NULL::numeric
            ELSE sum(opp_fgm) * 1.0 / sum(opp_fga)
        END AS opp_fg_pct,
        CASE
            WHEN sum(opp_fg3a) = 0::numeric THEN NULL::numeric
            ELSE sum(opp_fg3m) * 1.0 / sum(opp_fg3a)
        END AS opp_fg3_pct,
        CASE
            WHEN sum(opp_fta) = 0::numeric THEN NULL::numeric
            ELSE sum(opp_ftm) * 1.0 / sum(opp_fta)
        END AS opp_ft_pct
   FROM mart_booker_head_to_head_games
  GROUP BY season, opponent, context;