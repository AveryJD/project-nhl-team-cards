# ====================================================================================================
# SCRIPT TO GENERATE NHL TEAM CARDS
# ====================================================================================================

# Imports
from utils import card_generation

"""
Different functions for generating player cards:

card_generation.make_team_card('Toronto Maple Leafs', '2025-2026', 'light')
card_generation.make_all_team_cards('2025-2026', 'dark')
"""

# Generate team cards
card_generation.make_all_team_cards('2025-2026', 'dark')
