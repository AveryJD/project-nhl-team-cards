# ====================================================================================================
# FUNCTIONS FOR CALCULATING TEAM ELO RATINGS
# ====================================================================================================

# Imports
import pandas as pd
import numpy as np
import os
import constants
import load_save


DATA_DIR = constants.DATA_DIR

# Elo constants
INITIAL_ELO = constants.INITIAL_ELO
ELO_K = constants.ELO_K
ELO_S = constants.ELO_S
HOME_ADV = constants.ELO_HOME_ADV
ELO_RESULTS = constants.ELO_RESULTS


def get_expected_score(rating_a, rating_b, home_adv):
    expected_score = 1 / (1 + 10**((rating_b - (rating_a + home_adv)) / ELO_S))
    return expected_score


def get_margin_multiplier(goals_a, goals_b, rating_a, rating_b):
    # Get margin of victory
    margin = abs(goals_a - goals_b)
    # Get rating of winning and losing team
    if goals_a > goals_b:
        rating_w = rating_a
        rlating_l = rating_b
    else:
        rating_w = rating_b
        rlating_l = rating_a
    
    # Calculate margin multiplier
    numerator = (0.6686 * np.log(margin) + 0.8048) * 2.05
    denominator = (rating_w - rlating_l) * 0.001 + 2.05
    margin_multiplier = numerator / denominator
    return margin_multiplier


def calculate_season_elo(season):

    # Load games data
    df = load_save.load_games(season)

    # Get all teams that played in the given season
    teams_in_season = df['Team'].unique()

    # Initialize all Elo ratings at 1500
    current_ratings = {team: INITIAL_ELO for team in teams_in_season}

    # Initialize game counter and Elo ratings list for tracking
    team_game_counts = {team: 0 for team in teams_in_season}
    elo_history = {team: [] for team in teams_in_season}

    # Add initial Elo as game 0
    for team in teams_in_season:
        elo_history[team].append((0, INITIAL_ELO))

    # Group same games together (in data, each game appears twice)
    games = df.groupby('Game', sort=False)

    # For every game
    for _, game in games:
        # Get the home and away team names and scores from the game result string
        game_string = game.iloc[0]['Game']

        _, teams_part = game_string.split(' - ')
        away_part, home_part = teams_part.split(',')

        away_tokens = away_part.strip().split()
        home_tokens = home_part.strip().split()

        away_team_name = ' '.join(away_tokens[:-1])
        away_team_score = int(away_tokens[-1])

        home_team_name = ' '.join(home_tokens[:-1])
        home_team_score = int(home_tokens[-1])

        team_one = game.iloc[0]['Team']
        team_two = game.iloc[1]['Team']

        if home_team_name in team_one:          # Fix Utah Hockey Club and Coyotes team?
            home_team = team_one
            away_team = team_two
        else:
            home_team = team_two
            away_team = team_one

        # Get the ratings of both teams
        home_rating = current_ratings[home_team]
        away_rating = current_ratings[away_team]

        # Get the expected result for the home team based on ratings
        expected_home = get_expected_score(home_rating, away_rating, HOME_ADV)

        # Get the actual result based on score and when the game ended
        toi = game.iloc[0]['TOI']
        minutes, seconds = map(int, toi.split(':'))
        game_time = minutes + seconds / 60
        is_shootout = False
        if home_team_score > away_team_score and game_time <= 60:
            result_home = ELO_RESULTS.get('R Win')
        elif home_team_score > away_team_score and 60 < game_time < 65:
            result_home = ELO_RESULTS.get('OT Win')
        elif home_team_score > away_team_score and game_time >= 65:
            result_home = ELO_RESULTS.get('SO Win')
            is_shootout = True
        elif home_team_score < away_team_score and game_time <= 60:
            result_home = ELO_RESULTS.get('R Loss')
        elif home_team_score < away_team_score and 60 < game_time < 65:
            result_home = ELO_RESULTS.get('OT Loss')
        elif home_team_score < away_team_score and game_time >= 65:
            result_home = ELO_RESULTS.get('SO Loss')
            is_shootout = True
        else:
            result_home = 0.5

        # Calculate the margin multiplier
        if not is_shootout:
            margin_multiplier = get_margin_multiplier(home_team_score, away_team_score, home_rating, away_rating)
        else:
            margin_multiplier = 1.0

        # Calculate the Elo shift
        shift = ELO_K * (result_home - expected_home) * margin_multiplier

        # Apply the Elo shift to both teams
        current_ratings[home_team] += shift
        current_ratings[away_team] -= shift

        # Increment game counter and track elo for that game
        team_game_counts[home_team] += 1
        team_game_counts[away_team] += 1

        elo_history[home_team].append((team_game_counts[home_team], current_ratings[home_team]))
        elo_history[away_team].append((team_game_counts[away_team], current_ratings[away_team]))

    # Save CSVs
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, 'elo')
    os.makedirs(save_dir, exist_ok=True)

    # Fix inconsistent team names
    inverted_team_dict = {value: key for key, value in constants.TEAM_NAMES.items()}
    inverted_team_dict['Utah Hockey Club'] = 'UTA'
    inverted_team_dict['St Louis Blues'] = 'STL'

    # Save Elo results
    for team, history in elo_history.items():
        team_abreviation = inverted_team_dict.get(team)
        team_df = pd.DataFrame(history, columns=["Game", "Elo"])
        file_name = f'{season}_{team_abreviation}_elo.csv'
        load_save.save_csv(team_df, season, 'elo', file_name)

    return None



def main():
    # Calculate the Elo history of every team for every season
    seasons = constants.SEASONS
    for season in seasons:
        calculate_season_elo(season)


if __name__ == '__main__':
    main()
