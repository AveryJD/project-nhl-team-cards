# ====================================================================================================
# FUNCTIONS FOR LOADING AND SAVING DIFFERENT FILES
# ====================================================================================================

# Imports
import pandas as pd
from PIL import Image
import os
from team_card_project import constants

PROJECT_DIR = constants.PROJECT_DIR
DATA_DIR = constants.DATA_DIR


def load_card_data(season: str) -> pd.DataFrame:
    """
    Load processed team card data used for generating team cards.

    :param season: Season string ('YYYY-YYYY')
    :return: DataFrame containing team card metrics
    """
    file_name = f'{season}_team_card_data.csv'
    # Card data lives in data/card_data/team_card_data/ (the layout the stats collection project writes)
    file_path = os.path.join(DATA_DIR, 'card_data', 'team_card_data', file_name)
    df = pd.read_csv(file_path)
    return df


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
