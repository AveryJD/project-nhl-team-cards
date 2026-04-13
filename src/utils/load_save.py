# ====================================================================================================
# FUNCTIONS FOR LOADING AND SAVING DIFFERENT FILES
# ====================================================================================================

# Imports
import pandas as pd
from PIL import Image
import os
from utils import constants

PROJECT_DIR = constants.PROJECT_DIR
DATA_DIR = constants.DATA_DIR


def load_team_data(season: str, situation: str) -> pd.DataFrame:
    """
    Load team statistics data for a given season and situation.

    :param season: Season string ('YYYY-YYYY')
    :param situation: Game situation (e.g., '5v5', 'all')
    :return: DataFrame containing team statistics
    """
    file_name = f'{season}_{situation}_team_data.csv'
    file_path = os.path.join(DATA_DIR, 'team_card_data', season, 'results', file_name)
    df = pd.read_csv(file_path)
    return df
    

def load_games(season: str) -> pd.DataFrame:
    """
    Load game results data for a given season.

    :param season: Season string ('YYYY-YYYY')
    :return: DataFrame containing game results
    """
    file_name = f'{season}_games.csv'
    file_path = os.path.join(DATA_DIR, 'team_card_data', season, 'results', file_name)
    df = pd.read_csv(file_path)
    return df
    

def load_srs(season: str) -> pd.DataFrame:
    """
    Load Simple Rating System data for a given season.

    :param season: Season string ('YYYY-YYYY')
    :return: DataFrame containing SRS values
    """
    file_name = f'{season}_srs.csv'
    file_path = os.path.join(DATA_DIR, 'team_card_data', season, 'results', file_name)
    df = pd.read_csv(file_path)
    return df
    

def load_elo(season: str, team: str) -> pd.DataFrame:
    """
    Load Elo rating history for a specific team in a given season.

    :param season: Season string ('YYYY-YYYY')
    :param team: Team abbreviation
    :return: DataFrame containing Elo ratings over the season
    """
    file_name = f'{season}_{team}_elo.csv'
    file_path = os.path.join(DATA_DIR, 'team_card_data', season, 'elo', file_name)
    df = pd.read_csv(file_path)
    return df


def load_card_data(season: str) -> pd.DataFrame:
    """
    Load processed team card data used for generating team cards.

    :param season: Season string ('YYYY-YYYY')
    :return: DataFrame containing team card metrics
    """
    file_name = f'{season}_team_card_data.csv'
    file_path = os.path.join(DATA_DIR, 'team_card_data', 'card_data', file_name)
    df = pd.read_csv(file_path)
    return df


def save_csv(df: pd.DataFrame, season: str, sub_folder: str, file_name: str) -> None:
    """
    Save a DataFrame as a CSV file in a specified folder.

    :param df: The DataFrame to save
    :param sub_folder: Subfolder name inside the season folder
    :param file_name: Name of the CSV file to save
    :return: None
    """
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, sub_folder)
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, file_name)

    df.to_csv(save_path, index=False)
    print(f"Saved {file_name}")


def save_card_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save a DataFrame as a CSV file in a specified folder.

    :param df: The DataFrame to save
    :param file_name: Name of the CSV file to save
    :return: None
    """
    save_dir = os.path.join(DATA_DIR, 'team_card_data', 'card_data')
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, file_name)

    df.to_csv(save_path, index=False)
    print(f"Saved {file_name}")


def save_card(card: Image, season: str, file_name: str) -> None:
    """
    Save a card PNG to a specified folder.

    :param card: The card image to save
    :param season: The season folder to save to
    :param team: The team folder inside the year folder to save to 
    :param file_name: Name of the card to save
    :return: None
    """
    save_dir = os.path.join(PROJECT_DIR, 'team_cards', season)
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, file_name)

    card.save(save_path, 'PNG')
    print(f"Saved {file_name}")


def get_prev_season(cur_season: str) -> str:
    """
    Return the str for the previous season from a given season's str.

    :param cur_season: A str of the current season ('YYYY-YYYY')
    :return: A str of the season previous to the current season
    """
    start_year, end_year = map(int, cur_season.split("-"))
    prev_season = f"{start_year - 1}-{end_year - 1}"

    return prev_season