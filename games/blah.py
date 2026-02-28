import os
import time
import random
import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder
from requests.exceptions import ReadTimeout, ConnectionError

# ---------- config ----------
TEAM_ABBR = "WAS"
TEAM_ID = 1610612764

START_SEASON = 2015
END_SEASON = 2025  # 2025 means 2025-26

OUT_DIR = "to_games_csvs"
OUT_FILE = f"{TEAM_ABBR.lower()}_games_{START_SEASON}_{END_SEASON+1}.csv"

# throttling (bounded)
SLEEP_MIN = 1.1
SLEEP_MAX = 2.5

# retries
MAX_TRIES = 6
REQUEST_TIMEOUT = 90

# optional cooldown
COOLDOWN_EVERY = 40  # requests (WAS-only run is small)
COOLDOWN_SECONDS = 20
# ---------------------------

def season_str(year_start: int) -> str:
    """2015 -> '2015-16'"""
    return f"{year_start}-{str(year_start + 1)[-2:]}"

def sleepy():
    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

def fetch_team_games(team_id: int, season: str, season_type: str) -> pd.DataFrame:
    """
    season_type: 'Regular Season' or 'Playoffs'
    Retries on timeouts/connection issues and JSON decode issues.
    """
    delay = 2.0

    for attempt in range(1, MAX_TRIES + 1):
        try:
            finder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team_id,
                season_nullable=season,
                season_type_nullable=season_type,
                timeout=REQUEST_TIMEOUT
            )
            df = finder.get_data_frames()[0]
            df["SEASON"] = season
            df["SEASON_TYPE"] = season_type
            return df

        except (ReadTimeout, ConnectionError, TimeoutError, ValueError) as e:
            # ValueError often shows up as JSON decode issues: "Expecting value..."
            if attempt == MAX_TRIES:
                print(f"Failed after {MAX_TRIES} attempts: {season} {season_type} ({e})")
                return pd.DataFrame()

            wait = delay + random.uniform(0.0, 2.0)
            print(f"Retry {attempt}/{MAX_TRIES} for {season} {season_type}: {e}. Waiting {wait:.1f}s")
            time.sleep(wait)
            delay *= 2.0

        except Exception as e:
            print(f"Unexpected error for {season} {season_type}: {e}")
            return pd.DataFrame()

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # overwrite the existing WAS file
    out_path = os.path.join(OUT_DIR, OUT_FILE)
    if os.path.exists(out_path):
        os.remove(out_path)

    print(f"Re-pulling {TEAM_ABBR} (team_id={TEAM_ID}) seasons {START_SEASON}-{END_SEASON+1}")
    all_dfs = []
    req_count = 0

    for y in range(START_SEASON, END_SEASON + 1):
        season = season_str(y)
        print(f"Pulling {TEAM_ABBR} {season}")

        reg_df = fetch_team_games(TEAM_ID, season, "Regular Season")
        if not reg_df.empty:
            reg_df["TEAM_ABBR"] = TEAM_ABBR
            reg_df["TEAM_ID"] = TEAM_ID
            reg_df["TEAM_NAME"] = "Washington Wizards"
            all_dfs.append(reg_df)
            print(f"  Regular: {len(reg_df)}")
        else:
            print("  Regular: no data returned")

        req_count += 1
        sleepy()

        po_df = fetch_team_games(TEAM_ID, season, "Playoffs")
        if not po_df.empty:
            po_df["TEAM_ABBR"] = TEAM_ABBR
            po_df["TEAM_ID"] = TEAM_ID
            po_df["TEAM_NAME"] = "Washington Wizards"
            all_dfs.append(po_df)
            print(f"  Playoffs: {len(po_df)}")
        else:
            print("  Playoffs: no data returned")

        req_count += 1
        sleepy()

        if req_count % COOLDOWN_EVERY == 0:
            print(f"Cooldown... ({COOLDOWN_SECONDS}s)")
            time.sleep(COOLDOWN_SECONDS)

    if not all_dfs:
        print("No data returned for any season. Nothing to save.")
        return

    combined = pd.concat(all_dfs, ignore_index=True).drop_duplicates()
    combined.to_csv(out_path, index=False)

    print(f"Saved {TEAM_ABBR}: {out_path} | rows={len(combined)}")

if __name__ == "__main__":
    main()