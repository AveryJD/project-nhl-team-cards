# ====================================================================================================
# SCRIPT TO GENERATE NHL TEAM ELO AND SRS RATINGS AND ASSEMBLE CARD DATA
# ====================================================================================================

# Imports
from utils import elo
from utils import srs
from utils import card_data
from utils import constants


# Generate Elo ratings history
seasons = constants.DATA_SEASONS
for season in seasons:
    elo.calculate_season_elo(season)

# Generate SRS ratings
for season in constants.DATA_SEASONS:
    srs.calculate_season_srs(season)

# Assemble all card data
for season in constants.DATA_SEASONS:
    card_data.make_card_data(season)
