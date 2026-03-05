import pandas as pd
import numpy as np
import os
import constants

# Elo Constants
INITIAL_ELO = constants.INITIAL_ELO
ELO_K = constants.ELO_K
HOME_ADV = constants.ELO_HOME_ADV

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
    file_path = f'data/games/{season}_game_data.csv'
    if not os.path.exists(file_path):
        return pd.DataFrame()
        
    df = pd.read_csv(file_path)
    
    # Fresh initialization
    teams_in_season = df['Team'].unique()
    current_ratings = {}
    for team in teams_in_season:
        current_ratings[team] = INITIAL_ELO
            
    # Group games together (they appear in rows of 2)
    games = df.groupby('Game', sort=False)

    for _, game in games:
        game_name = game.iloc[0]['Game']
        home_team_name = game_name[5]

        # Get home team and away team
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

        # Get team ratings
        away_team_rating = current_ratings[away_team]
        home_team_rating = current_ratings[home_team]

        # Get team goals for in the game
        gf_away = game.iloc[away_index]['GF']
        gf_home = game.iloc[home_index]['GF']

        # Calculate elo shift for the home team
        home_team_expected_score = get_expected_score(home_team_rating, away_team_rating, HOME_ADV)

        if gf_home > gf_away:
            home_team_result = 1
        elif gf_home < gf_away:
            home_team_result = 0
        else:
            home_team_result = 0.5

        margin_multiplier = get_margin_multiplier(gf_home, gf_away, home_team_rating, away_team_rating)
        home_team_shift = ELO_K * (home_team_result - home_team_expected_score) * margin_multiplier

        # Shift elo for each team
        current_ratings[home_team] += home_team_shift
        current_ratings[away_team] -= home_team_shift

    # Capture end of season state
    season_snapshot = [{"Season": season, "Team": team, "Elo": current_ratings[team]} for team in teams_in_season]

    elo_df = pd.DataFrame(season_snapshot)
    return elo_df


def main():
    all_season_results = []

    seasons = constants.SEASONS

    for season in seasons:
        season_df = calculate_season_elo(season)
        
        all_season_results.append(season_df)

    final_df = pd.concat(all_season_results, ignore_index=True)
    
    # Make season first column
    cols = ['Season', 'Team', 'Elo']
    final_df = final_df[cols]
    
    # Sort by season then highest elo
    final_df = final_df.sort_values(by=['Season', 'Elo'], ascending=[False, False])

    os.makedirs('data/output', exist_ok=True)
    final_df.to_csv('data/output/elo_results.csv', index=False)


if __name__ == '__main__':
    main()