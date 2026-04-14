# ====================================================================================================
# FUNCTIONS FOR CALCULATING TEAM SIMPLE RATING SYSTEM RATINGS
# ====================================================================================================

# Imports
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from team_card_project.utils import constants
from team_card_project.utils import load_save


DATA_DIR = constants.DATA_DIR


def sum_of_squared_residuals(params, games):
    """
    Objective function for the SRS optimization.
    Calculates the sum of squared residuals between predicted and actual
    goal margins across all games.

    :param params: Array containing home-ice advantage followed by team ratings
    :param games: List of dictionaries containing home team index, away team index, and margin
    :return: Sum of squared residuals
    """
    # Get ratings and home advantage
    home_adv = params[0]
    ratings = params[1:]
    
    # Calculate the SSR
    ssr = 0
    for game in games:
        prediction = (ratings[game["home_idx"]] - ratings[game["away_idx"]]) + home_adv
        ssr += (game["margin"] - prediction) ** 2

    return ssr


def calculate_srs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Simple Rating System (SRS) ratings for teams based on game results.
    The model estimates a rating for each team and a home-ice advantage value by
    minimizing the sum of squared residuals between actual goal margins and predicted margins.

    :param df: DataFrame containing game-level team results
    :return: DataFrame containing each team's SRS rating
    """

    # Get all teams that played in the given season
    teams_in_season = sorted(set(df["Home Team"].unique()))
    team_to_idx = {team: i for i, team in enumerate(teams_in_season)}
    num_teams = len(teams_in_season)
    games = []

    for _, row in df.iterrows():
        games.append({
            "home_idx": team_to_idx[row["Home Team"]],
            "away_idx": team_to_idx[row["Away Team"]],
            "margin": row["Home Score"] - row["Away Score"]
        })

    # Constrain ratings so the average rating equals zero
    constraints = ({'type': 'eq', 'fun': lambda params: np.mean(params[1:])})

    initial_guess = np.zeros(num_teams + 1)

    # Run optimization to estimate ratings
    result = minimize(
        sum_of_squared_residuals,
        initial_guess,
        args=(games,),
        constraints=constraints,
        method="SLSQP"
    )

    ratings_final = result.x[1:]

    results = []

    # Store results for each team
    for i, team in enumerate(teams_in_season):
        results.append({
            "Team": team,
            "SRS Rating": round(ratings_final[i], 3)
        })

    return pd.DataFrame(results)


def calculate_season_srs(season: str) -> None:
    """
    Calculate and save SRS ratings for a given NHL season.

    :param season: Season string formatted as 'YYYY-YYYY'
    :return: None
    """

    # Load game  results
    games_df = load_save.load_games(season)

    # Calculate Simple Rating System ratings
    srs_df = calculate_srs(games_df)

    # Add season column
    srs_df.insert(0, "Season", season)

    # Rank teams by SRS rating
    srs_df = srs_df.sort_values(by="SRS Rating", ascending=False)
    srs_df["SRS Rank"] = range(1, len(srs_df) + 1)

    # Save SRS results
    file_name = f"{season}_srs.csv"
    load_save.save_csv(srs_df, season, 'ratings', file_name)

    return None