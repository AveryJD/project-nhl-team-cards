# ====================================================================================================
# FUNCTIONS FOR GENERATING DIFFERENT SETS OF PLAYER CARDS
# ====================================================================================================

# Imports
from utils import card_functions as cf
from utils import constants

DATA_DIR = constants.DATA_DIR


def make_team_card(team_name: str, season: str, mode: str = 'light') -> None:
    """
    Generate a player card for a specific team.

    :param player_name: A str of the team's full name ('Location Name')
    :param season: A str representing the season ('YYYY-YYYY')
    :param mode: A str determining the style of card ('light' or 'dark')
    :return: None
    """
    cf.make_team_card(team_name, season, mode=mode)


def make_all_team_cards(season: str, mode: str = 'light') -> None:
    """
    Generate team cards for every team in a given season.

    :param season: A str representing the season ('YYYY-YYYY')
    :param mode: A str determining the style of card ('light' or 'dark')
    :return: None
    """
    for team in constants.TEAM_NAMES:
        team_name = constants.TEAM_NAMES.get(team)
        if team_name in constants.TEAM_DIVISION_BY_SEASON.get(season):
            cf.make_team_card(team_name, season, mode)
