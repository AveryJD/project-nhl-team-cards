# ====================================================================================================
# Functions
# ====================================================================================================

# Imports
import pandas as pd
import numpy as np
import os
import constants

# Elo Constants
INITIAL_ELO = constants.INITIAL_ELO
ELO_K = constants.ELO_K
HOME_ADV = constants.ELO_HOME_ADV

DATA_DIR = constants.DATA_DIR

def get_expected_score(ra, rb, home_adv):
    expected_score = 1 / (1 + 10**((rb - (ra + home_adv)) / 400))
    return expected_score

def get_margin_multiplier(gf, ga, ra, rb):
    margin = abs(gf - ga)
    if margin <= 1:
        return 1.0
    rw = ra if gf > ga else rb
    rl = rb if gf > ga else ra
    
    numerator = (0.6686 * np.log(margin) + 0.8048) * 2.05
    denominator = (rw - rl) * 0.001 + 2.05
    margin_multiplier = numerator / denominator
    return margin_multiplier


def calculate_season_elo(season):
    file_path = f'team_card_data/{season}/games/{season}_game_data.csv'
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)

    teams_in_season = df['Team'].unique()

    current_ratings = {team: INITIAL_ELO for team in teams_in_season}
    team_game_counts = {team: 0 for team in teams_in_season}
    elo_history = {team: [] for team in teams_in_season}

    # Add initial Elo as game 0
    for team in teams_in_season:
        elo_history[team].append((0, INITIAL_ELO))

    games = df.groupby('Game', sort=False)

    for _, game in games:
        game_name = game.iloc[0]['Game']
        home_team_name = game_name[5]

        team_one = game.iloc[0]['Team']
        team_two = game.iloc[1]['Team']

        if team_one.split()[1] == home_team_name:
            away_team = team_one
            home_team = team_two
            away_index = 0
            home_index = 1
        else:
            away_team = team_two
            home_team = team_one
            away_index = 1
            home_index = 0

        away_rating = current_ratings[away_team]
        home_rating = current_ratings[home_team]

        gf_away = game.iloc[away_index]['GF']
        gf_home = game.iloc[home_index]['GF']

        expected_home = get_expected_score(home_rating, away_rating, HOME_ADV)

        if gf_home > gf_away:
            result_home = 1
        elif gf_home < gf_away:
            result_home = 0
        else:
            result_home = 0.5

        margin_multiplier = get_margin_multiplier(gf_home, gf_away, home_rating, away_rating)
        shift = ELO_K * (result_home - expected_home) * margin_multiplier

        current_ratings[home_team] += shift
        current_ratings[away_team] -= shift

        team_game_counts[home_team] += 1
        team_game_counts[away_team] += 1

        elo_history[home_team].append((team_game_counts[home_team], current_ratings[home_team]))
        elo_history[away_team].append((team_game_counts[away_team], current_ratings[away_team]))

    # Save CSVs
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, 'elo')
    os.makedirs(save_dir, exist_ok=True)

    for team, history in elo_history.items():
        team_df = pd.DataFrame(history, columns=["Game", "Elo"])
        file_name = team.replace(" ", "_") + ".csv"
        save_path = os.path.join(save_dir, file_name)
        team_df.to_csv(save_path, index=False)

    return None


def main():
    seasons = constants.SEASONS

    for season in seasons:
        calculate_season_elo(season)


if __name__ == '__main__':
    main()
