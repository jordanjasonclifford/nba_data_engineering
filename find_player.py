from nba_api.stats.static import players

# Search by name
booker = players.find_players_by_full_name("Zion Williamson")

print(booker)