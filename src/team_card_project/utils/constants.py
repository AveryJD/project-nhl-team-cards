# ====================================================================================================
# CONSTANTS
# ====================================================================================================

# Imports
import os

def find_project_dir(start_dir: str) -> str:
    """
    Traverse upward until a directory containing 'data' is found.

    :param start_dir: Directory where the search starts
    :return: Project root directory
    """

    while True:
        potential_data_dir = os.path.join(start_dir, 'data')

        if os.path.exists(potential_data_dir):
            return start_dir

        parent = os.path.dirname(start_dir)

        if parent == start_dir:
            raise FileNotFoundError('Could not find "data" folder')

        start_dir = parent


# Directory of the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Root project directory
PROJECT_DIR = find_project_dir(CURRENT_DIR)

# Data directory
DATA_DIR = os.path.join(PROJECT_DIR, 'data')



# ====================================================================================================
# CARD DATA CONSTANTS
# ====================================================================================================

# Date card data was updated on
UPDATE_DATE = 'April 17, 2026'

# Situations to scrape team data for
SITUATIONS = ['all', '5v5', '4v5', '5v4']

# Seasons to scrape data for
DATA_SEASONS = ['2025-2026']

# Seasons to gather card data for
CARD_SEASONS = [
    '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', 
    '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', 
    '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', 
    '2022-2023', '2023-2024', '2024-2025', '2025-2026'
]

# All seasons of avalible data
ALL_SEASONS = [
    '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', 
    '2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017', 
    '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022', 
    '2022-2023', '2023-2024', '2024-2025', '2025-2026'
]



# ====================================================================================================
# ELO CONSTANTS
# ====================================================================================================

INITIAL_ELO = 1500
ELO_K = 20
ELO_S = 400
ELO_HOME_ADV = 30

ELO_RESULTS = {
    'R Win': 1.0,
    'OT Win': 0.9,
    'SO Win': 0.7,
    'SO Loss': 0.3,
    'OT Loss': 0.1,
    'R Loss': 0.0
}



# ====================================================================================================
# CARD DESIGN CONSTANTS
# ====================================================================================================

# Attribute names with full names (CHANGE FOR TEAMS)
ATTRIBUTE_NAMES = {
    'gf_rank' : 'Goals For',
    'ga_rank' : 'Goals Against',
    'xgf_rank' : 'xGoals For',
    'xga_rank' : 'xGoals Against',
    'pp_rank' : 'Power Play',
    'pk_rank' : 'Penalty Kill',
    'sf_rank' : 'Shots For',
    'sa_rank' : 'Shots Against',
    'fn_rank' : 'Finishing',
    'gt_rank' : 'Goaltending',
}

# Card color RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK = (39, 39, 39)
GRAPH_WHITE = (255/255, 255/255, 255/255)
GRAPH_BLACK = (0/255, 0/255, 0/255)
GRAPH_GRAY = (180/255, 180/255, 180/255)
GRAPH_DARK = (39/255, 39/255, 39/255)
GRAPH_RED = (255/255, 70/255, 70/255)
GRAPH_BLUE = (70/255, 70/255, 255/255)

# Team primary color RBG values
PRIMARY_COLORS = {
    'ANA': (252, 76, 2),    'ARI': (140, 38, 51),   'BOS': (252, 181, 20),
    'BUF': (0, 48, 135),    'CGY': (210, 0, 28),    'CAR': (206, 17, 38),
    'CHI': (207, 10, 44),   'COL': (111, 38, 61),   'CBJ': (0, 38, 84),
    'DAL': (0, 104, 71),    'DET': (206, 17, 38),   'EDM': (252, 76, 0),
    'FLA': (200, 16, 46),   'LAK': (162,170,173),   'MIN': (2, 73, 48),
    'MTL': (175, 30, 45),   'NSH': (255, 184, 28),  'NJD': (206, 17, 38),
    'NYI': (244, 125, 48),  'NYR': (0, 56, 168),    'OTT': (218, 26, 50),
    'PHI': (247, 73, 2),    'PIT': (252, 181, 20),  'SJS': (0, 109, 117),
    'SEA': (153, 217, 217), 'STL': (0, 47, 135),    'TBL': (0, 40, 104),
    'TOR': (0, 32, 91),     'VAN': (0, 32, 91),     'UTA': (105, 179, 231),
    'VGK': (185, 151, 91),  'WSH': (4, 30, 66),     'WPG': (4, 30, 66),
    'ATL': (4, 30, 66),     'PHX': (140, 38, 51)
}

# Team secondary colors RGB values
SECONDARY_COLORS = {
    'ANA': (185, 151, 91),  'ARI': (21,71,52),      'BOS': (17, 17, 17),
    'BUF': (255, 184, 28),  'CGY': (250, 175, 25),  'CAR': (0, 0, 0),
    'CHI': (0, 0, 0),       'COL': (35, 97, 146),   'CBJ': (206,17,38),
    'DAL': (143, 143, 140), 'DET': (0, 0, 0),       'EDM': (4, 30, 66),
    'FLA': (4,30,66),       'LAK': (17, 17, 17),    'MIN': (175, 35, 36),
    'MTL': (25, 33, 104),   'NSH': (4,30,66),       'NJD': (0, 0, 0),
    'NYI': (0,83,155),      'NYR': (206,17,38),     'OTT': (0, 0, 0),
    'PHI': (0, 0, 0),       'PIT': (0, 0, 0),       'SJS': (0, 0, 0),
    'SEA': (0, 22, 40),     'STL': (252, 181, 20),  'TBL': (0, 0, 0),
    'TOR': (0, 0, 0),       'VAN': (0, 132, 61),    'UTA': (0, 0, 0),
    'VGK': (51,63,72),      'WSH': (200, 16, 46),   'WPG': (172,22,44),
    'ATL': (184, 97, 37),   'PHX': (21,71,52)
}



# ====================================================================================================
# TEAMS, DIVISIONS, AND NUMBER OF GAMES PER SEASON
# ====================================================================================================

# All NHL team abbreviations and full team names
TEAM_NAMES = {
    'ANA': 'Anaheim Ducks',        'BOS': 'Boston Bruins',        'BUF': 'Buffalo Sabres',        'CGY': 'Calgary Flames',
    'CAR': 'Carolina Hurricanes',  'CHI': 'Chicago Blackhawks',   'COL': 'Colorado Avalanche',    'CBJ': 'Columbus Blue Jackets',
    'DAL': 'Dallas Stars',         'DET': 'Detroit Red Wings',    'EDM': 'Edmonton Oilers',       'FLA': 'Florida Panthers',
    'LAK': 'Los Angeles Kings',    'MIN': 'Minnesota Wild',       'MTL': 'Montreal Canadiens',    'NSH': 'Nashville Predators',
    'NJD': 'New Jersey Devils',    'NYI': 'New York Islanders',   'NYR': 'New York Rangers',      'OTT': 'Ottawa Senators',
    'PHI': 'Philadelphia Flyers',  'PIT': 'Pittsburgh Penguins',  'SJS': 'San Jose Sharks',       'SEA': 'Seattle Kraken',
    'STL': 'St. Louis Blues',      'TBL': 'Tampa Bay Lightning',  'TOR': 'Toronto Maple Leafs',   'VAN': 'Vancouver Canucks',
    'UTA': 'Utah Mammoth',         'VGK': 'Vegas Golden Knights', 'WSH': 'Washington Capitals',   'WPG': 'Winnipeg Jets',
    'ARI': 'Arizona Coyotes',      'ATL': 'Atlanta Thrashers',    'PHX': 'Phoenix Coyotes'
}

TEAM_NAME_FIXES = {
    'St Louis Blues': 'St. Louis Blues',
    'Utah Hockey Club': 'Utah Mammoth',
}

GAME_TEAM_NAME_FIXES = {
    'Avalanche': 'Colorado Avalanche',
    'Blackhawks': 'Chicago Blackhawks',
    'Blue Jackets': 'Columbus Blue Jackets',
    'Blues': 'St. Louis Blues',
    'Bruins': 'Boston Bruins',
    'Canadiens': 'Montreal Canadiens',
    'Canucks': 'Vancouver Canucks',
    'Capitals': 'Washington Capitals',
    'Coyotes': 'Arizona Coyotes', # Phoenix Coyotes before 2014-2015
    'Devils': 'New Jersey Devils',
    'Ducks': 'Anaheim Ducks',
    'Flames': 'Calgary Flames',
    'Flyers': 'Philadelphia Flyers',
    'Golden Knights': 'Vegas Golden Knights',
    'Utah HC': 'Utah Mammoth',
    'Hurricanes': 'Carolina Hurricanes',
    'Islanders': 'New York Islanders',
    'Kings': 'Los Angeles Kings',
    'Kraken': 'Seattle Kraken',
    'Jets': 'Winnipeg Jets',
    'Lightning': 'Tampa Bay Lightning',
    'Mammoth': 'Utah Mammoth',
    'Maple Leafs': 'Toronto Maple Leafs',
    'Oilers': 'Edmonton Oilers',
    'Panthers': 'Florida Panthers',
    'Penguins': 'Pittsburgh Penguins',
    'Predators': 'Nashville Predators',
    'Rangers': 'New York Rangers',
    'Red Wings': 'Detroit Red Wings',
    'Sabres': 'Buffalo Sabres',
    'Senators': 'Ottawa Senators',
    'Sharks': 'San Jose Sharks',
    'Stars': 'Dallas Stars',
    'Thrashers': 'Atlanta Thrashers',
    'Wild': 'Minnesota Wild',
}

# Games per season
SEASON_GAMES = {
    '2025-2026': 82,    # Current season (max games any team has played)
    '2024-2025': 82,
    '2023-2024': 82,
    '2022-2023': 82,
    '2021-2022': 82,
    '2020-2021': 56,    # Shortened due to COVID
    '2019-2020': 71,    # Season paused due to COVID
    '2018-2019': 82,
    '2017-2018': 82,
    '2016-2017': 82,
    '2015-2016': 82,
    '2014-2015': 82,
    '2013-2014': 82,
    '2012-2013': 48,    # Shortened due to lockout
    '2011-2012': 82,
    '2010-2011': 82,
    '2009-2010': 82,
    '2008-2009': 82,
    '2007-2008': 82
}

# Teams per season
SEASON_TEAM_NUM = {
    '2025-2026': 32,
    '2024-2025': 32,
    '2023-2024': 32,
    '2022-2023': 32,
    '2021-2022': 32,    # Seattle Kraken Added
    '2020-2021': 31,  
    '2019-2020': 31,  
    '2018-2019': 31,
    '2017-2018': 31,    # Vegas Golden Knights Added
    '2016-2017': 30,
    '2015-2016': 30,
    '2014-2015': 30,
    '2013-2014': 30,
    '2012-2013': 30,
    '2011-2012': 30,
    '2010-2011': 30,
    '2009-2010': 30,
    '2008-2009': 30,
    '2007-2008': 30
}

# Division to conference map
DIVISION_CONFERENCE = {
    'Atlantic': 'Eastern',
    'Metropolitan': 'Eastern',
    'Northeast': 'Eastern',
    'Southeast': 'Eastern',

    'Central': 'Western',
    'Northwest': 'Western',
    'Pacific': 'Western'
}

# Team to division maps
TEAM_DIVISION_MODERN_BASE = {
    'Boston Bruins': 'Atlantic',
    'Buffalo Sabres': 'Atlantic',
    'Detroit Red Wings': 'Atlantic',
    'Florida Panthers': 'Atlantic',
    'Montreal Canadiens': 'Atlantic',
    'Ottawa Senators': 'Atlantic',
    'Tampa Bay Lightning': 'Atlantic',
    'Toronto Maple Leafs': 'Atlantic',

    'Carolina Hurricanes': 'Metropolitan',
    'Columbus Blue Jackets': 'Metropolitan',
    'New Jersey Devils': 'Metropolitan',
    'New York Islanders': 'Metropolitan',
    'New York Rangers': 'Metropolitan',
    'Philadelphia Flyers': 'Metropolitan',
    'Pittsburgh Penguins': 'Metropolitan',
    'Washington Capitals': 'Metropolitan',

    'Chicago Blackhawks': 'Central',
    'Colorado Avalanche': 'Central',
    'Dallas Stars': 'Central',
    'Minnesota Wild': 'Central',
    'Nashville Predators': 'Central',
    'St. Louis Blues': 'Central',
    'Winnipeg Jets': 'Central',

    'Anaheim Ducks': 'Pacific',
    'Calgary Flames': 'Pacific',
    'Edmonton Oilers': 'Pacific',
    'Los Angeles Kings': 'Pacific',
    'San Jose Sharks': 'Pacific',
    'Vancouver Canucks': 'Pacific',
}

TEAM_DIVISION_UTAH = {
    **TEAM_DIVISION_MODERN_BASE,
    'Utah Mammoth': 'Central',
    'Seattle Kraken': 'Pacific',
    'Vegas Golden Knights': 'Pacific',
}

TEAM_DIVISION_SEATTLE = {
    **TEAM_DIVISION_MODERN_BASE,
    'Arizona Coyotes': 'Central',
    'Seattle Kraken': 'Pacific',
    'Vegas Golden Knights': 'Pacific',
}

TEAM_DIVISION_COVID = {
    'Calgary Flames': 'North',
    'Edmonton Oilers': 'North',
    'Montreal Canadiens': 'North',
    'Ottawa Senators': 'North',
    'Toronto Maple Leafs': 'North',
    'Vancouver Canucks': 'North',
    'Winnipeg Jets': 'North',

    'Boston Bruins': 'East',
    'Buffalo Sabres': 'East',
    'New Jersey Devils': 'East',
    'New York Islanders': 'East',
    'New York Rangers': 'East',
    'Philadelphia Flyers': 'East',
    'Pittsburgh Penguins': 'East',
    'Washington Capitals': 'East',

    'Carolina Hurricanes': 'Central',
    'Chicago Blackhawks': 'Central',
    'Columbus Blue Jackets': 'Central',
    'Dallas Stars': 'Central',
    'Detroit Red Wings': 'Central',
    'Florida Panthers': 'Central',
    'Nashville Predators': 'Central',
    'Tampa Bay Lightning': 'Central',

    'Anaheim Ducks': 'West',
    'Arizona Coyotes': 'West',
    'Colorado Avalanche': 'West',
    'Los Angeles Kings': 'West',
    'Minnesota Wild': 'West',
    'St. Louis Blues': 'West',
    'San Jose Sharks': 'West',
    'Vegas Golden Knights': 'West'
}

TEAM_DIVISION_VEGAS = {
    **TEAM_DIVISION_MODERN_BASE,
    'Arizona Coyotes': 'Pacific',
    'Vegas Golden Knights': 'Pacific',
}

TEAM_DIVISION_ARIZONA = {
    **TEAM_DIVISION_MODERN_BASE,
    'Arizona Coyotes': 'Pacific',
}

TEAM_DIVISION_PHOENIX = {
    **TEAM_DIVISION_MODERN_BASE,
    'Phoenix Coyotes': 'Pacific',
}

TEAM_DIVISION_WINNIPEG = {
    'New Jersey Devils': 'Atlantic',
    'New York Islanders': 'Atlantic',
    'New York Rangers': 'Atlantic',
    'Philadelphia Flyers': 'Atlantic',
    'Pittsburgh Penguins': 'Atlantic',

    'Boston Bruins': 'Northeast',
    'Buffalo Sabres': 'Northeast',
    'Montreal Canadiens': 'Northeast',
    'Ottawa Senators': 'Northeast',
    'Toronto Maple Leafs': 'Northeast',

    'Carolina Hurricanes': 'Southeast',
    'Florida Panthers': 'Southeast',
    'Tampa Bay Lightning': 'Southeast',
    'Washington Capitals': 'Southeast',
    'Winnipeg Jets': 'Southeast',

    'Chicago Blackhawks': 'Central',
    'Columbus Blue Jackets': 'Central',
    'Detroit Red Wings': 'Central',
    'Nashville Predators': 'Central',
    'St. Louis Blues': 'Central',

    'Calgary Flames': 'Northwest',
    'Colorado Avalanche': 'Northwest',
    'Edmonton Oilers': 'Northwest',
    'Minnesota Wild': 'Northwest',
    'Vancouver Canucks': 'Northwest',

    'Anaheim Ducks': 'Pacific',
    'Dallas Stars': 'Pacific',
    'Los Angeles Kings': 'Pacific',
    'Phoenix Coyotes': 'Pacific',
    'San Jose Sharks': 'Pacific',
}

TEAM_DIVISION_ATLANTA = {
    'New Jersey Devils': 'Atlantic',
    'New York Islanders': 'Atlantic',
    'New York Rangers': 'Atlantic',
    'Philadelphia Flyers': 'Atlantic',
    'Pittsburgh Penguins': 'Atlantic',

    'Boston Bruins': 'Northeast',
    'Buffalo Sabres': 'Northeast',
    'Montreal Canadiens': 'Northeast',
    'Ottawa Senators': 'Northeast',
    'Toronto Maple Leafs': 'Northeast',

    'Atlanta Thrashers': 'Southeast',
    'Carolina Hurricanes': 'Southeast',
    'Florida Panthers': 'Southeast',
    'Tampa Bay Lightning': 'Southeast',
    'Washington Capitals': 'Southeast',

    'Chicago Blackhawks': 'Central',
    'Columbus Blue Jackets': 'Central',
    'Detroit Red Wings': 'Central',
    'Nashville Predators': 'Central',
    'St. Louis Blues': 'Central',

    'Calgary Flames': 'Northwest',
    'Colorado Avalanche': 'Northwest',
    'Edmonton Oilers': 'Northwest',
    'Minnesota Wild': 'Northwest',
    'Vancouver Canucks': 'Northwest',

    'Anaheim Ducks': 'Pacific',
    'Dallas Stars': 'Pacific',
    'Los Angeles Kings': 'Pacific',
    'Phoenix Coyotes': 'Pacific',
    'San Jose Sharks': 'Pacific',
}

TEAM_DIVISION_BY_SEASON = {
    '2025-2026': TEAM_DIVISION_UTAH,
    '2024-2025': TEAM_DIVISION_UTAH,
    '2023-2024': TEAM_DIVISION_SEATTLE,
    '2022-2023': TEAM_DIVISION_SEATTLE,
    '2021-2022': TEAM_DIVISION_SEATTLE,
    '2020-2021': TEAM_DIVISION_COVID,
    '2019-2020': TEAM_DIVISION_VEGAS,
    '2018-2019': TEAM_DIVISION_VEGAS,
    '2017-2018': TEAM_DIVISION_VEGAS,
    '2016-2017': TEAM_DIVISION_ARIZONA,
    '2015-2016': TEAM_DIVISION_ARIZONA,
    '2014-2015': TEAM_DIVISION_ARIZONA,
    '2013-2014': TEAM_DIVISION_PHOENIX,
    '2012-2013': TEAM_DIVISION_WINNIPEG,
    '2011-2012': TEAM_DIVISION_WINNIPEG,
    '2010-2011': TEAM_DIVISION_ATLANTA,
    '2009-2010': TEAM_DIVISION_ATLANTA,
    '2008-2009': TEAM_DIVISION_ATLANTA,
    '2007-2008': TEAM_DIVISION_ATLANTA,
}
