# ====================================================================================================
# SCRIPT TO GENERATE NHL TEAM ELO AND SRS RATINGS AND ASSEMBLE CARD DATA
# ====================================================================================================

# Imports
from utils import elo
from utils import srs
from utils import card_data
from utils import constants


# Generate team analytics and assemble card data
for season in constants.DATA_SEASONS:
    # Generate Elo ratings history
    elo.calculate_season_elo(season)

    # Generate SRS ratings
    srs.calculate_season_srs(season)

    # Assemble all card data
    card_data.make_card_data(season)
