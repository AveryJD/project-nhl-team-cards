# ====================================================================================================
# SCRIPT TO SCRAPE NHL TEAM DATA
# ====================================================================================================

# Imports
from utils import scrape_data
from utils import collect_logos
from utils import constants


# Scrape logos from NHL.com
collect_logos.scrape_logos()

# Gather team data from NaturalStatTrick
for season in constants.DATA_SEASONS:

    scrape_data.scrape_games_data(season)

    for situation in constants.SITUATIONS:
        scrape_data.scrape_team_data(season, situation)