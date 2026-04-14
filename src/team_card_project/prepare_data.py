# ====================================================================================================
# SCRIPT TO GENERATE NHL TEAM ELO AND SRS RATINGS AND ASSEMBLE CARD DATA
# ====================================================================================================

# Imports
from team_card_project.utils import elo
from team_card_project.utils import srs
from team_card_project.utils import card_data
from team_card_project.utils import constants


# Generate team analytics and assemble card data
for season in constants.DATA_SEASONS:
    # Generate Elo ratings history
    elo.calculate_season_elo(season)

    # Generate SRS ratings
    srs.calculate_season_srs(season)

    # Assemble all card data
    card_data.make_card_data(season)
