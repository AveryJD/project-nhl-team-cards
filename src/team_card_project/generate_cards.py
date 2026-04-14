# ====================================================================================================
# SCRIPT TO GENERATE NHL TEAM CARDS
# ====================================================================================================

# Imports
from team_card_project.utils import card_generation
from team_card_project.utils import constants

"""
Different functions for generating player cards:

card_generation.make_team_card('Toronto Maple Leafs', '2025-2026', 'light')
card_generation.make_all_team_cards('2025-2026', 'dark')
"""

# Generate all team cards
for season in constants.DATA_SEASONS:
    card_generation.make_all_team_cards(season, 'dark')
