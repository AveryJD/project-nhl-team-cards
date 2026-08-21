# ====================================================================================================
# SCRIPT TO SCRAPE NHL TEAM DATA
# ====================================================================================================

# Imports
from team_card_project.collect_data import scrape_data
from team_card_project.collect_data import collect_logos
from team_card_project import constants



if __name__ == '__main__':

    """
    # Scrape logos from NHL.com
    collect_logos.scrape_logos()
    """

    # Gather team data from NaturalStatTrick
    for season in constants.DATA_SEASONS:

        # Gather standings data
        scrape_data.scrape_standings_data(season)
        # Gather games data
        scrape_data.scrape_games_data(season)
        # Gather team statistics for multiple situations
        for situation in constants.SITUATIONS:
            scrape_data.scrape_team_data(season, situation)
