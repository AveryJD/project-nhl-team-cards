# ====================================================================================================
# FUNCTIONS FOR SCRAPING DATA FROM NATURALSTATTRICK
# ====================================================================================================

# Imports
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import random
import re
from team_card_project.utils import constants
from team_card_project.utils import load_save


DATA_DIR = constants.DATA_DIR


def random_delay() -> None:
    """
    Introduce a random delay between web requests to reduce server load and avoid rate limiting.

    :return: None
    """
    # Make delay by a random time of 10-20 seconds
    delay = random.uniform(10, 20)
    print(f'Waiting {delay:.2f} seconds before next request')
    time.sleep(delay)


def get_page(url: str) -> bytes:
    """
    Fetch the HTML content of a given URL.

    :param url: The URL to fetch
    :return: The content of the fetched page
    """
    # Delay before fetching the page
    random_delay()

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/123.0.0.0 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/avif,image/webp,*/*;q=0.8'
        ),
        'Accept-Language': 'en-CA,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://www.naturalstattrick.com/',
        'Connection': 'keep-alive',
    }

    # Fetch the page content
    with requests.Session() as session:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.content
    

def fix_team_names(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Replace team names in the specified columns for consistency.

    :param df: DataFrame to update
    :param columns: Columns that contain team names
    :return: Updated DataFrame
    """
    # Fix team names
    for col in columns:
        df[col] = df[col].replace(constants.TEAM_NAME_FIXES)
    
    return df


def scrape_data(url: str) -> pd.DataFrame:
    """
    Scrape table data from a given URL and return it as a DataFrame.

    :param url: The URL to scrape
    :return: DataFrame containing the scraped table data
    """
    # Fetch the page from the URL
    page_content = get_page(url)
    
    # Scrape page
    soup = BeautifulSoup(page_content, 'html.parser')
    columns = [item.text for item in soup.find_all('th')]
    data = [e.text for e in soup.find_all('td')]

    # Make DataFrame
    table = [data[i:i+len(columns)] for i in range(0, len(data), len(columns))]
    df = pd.DataFrame(table, columns=columns)
    
    return df


def scrape_team_data(season: str, situation: str) -> None:
    """
    Scrape team statistics for a given season and game situation, then save the results as a CSV.

    :param season: Season string ('YYYY-YYYY')
    :param situation: Game situation code used by Natural Stat Trick (e.g., 'all', '5v5', '5v4', '4v5')
    :return: None
    """

    url_season = season.replace('-', '')
    url = f'https://www.naturalstattrick.com/teamtable.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit={situation}&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td='

    df = scrape_data(url)

    df['Points'] = pd.to_numeric(df['Points'])
    df = df.sort_values(by='Points', ascending=False)

    df = df.drop(df.columns[0], axis=1)

    # Fix inconsistent team names
    df = fix_team_names(df, ['Team'])

    # Save as a CSV
    file_name = f'{season}_{situation}_team_data.csv'
    load_save.save_csv(df, season, 'scraped_data', file_name)

    return None


def scrape_standings_data(season: str) -> None:
    """
    Scrape league standings data for a given season and save the results as a CSV.

    :param season: Season string ('YYYY-YYYY')
    :return: None
    """

    url_season = season.replace('-', '')
    url = f'https://www.naturalstattrick.com/standings.php?season={url_season}&type=pts&disp=league'

    df = scrape_data(url)

    # Remove playoff/elimination prefixes from team names
    df['Team'] = df['Team'].str.replace(r'^[a-z]\s*-\s*', '', regex=True)
    df['Team'] = df['Team'].str.strip()

    # Keep NHL teams only (special case with Four Nations teams)
    df = df[df['Games Played'] != '0']

    # Fix inconsistent team names
    df = fix_team_names(df, ['Team'])

    # Save as a CSV
    file_name = f'{season}_standings.csv'
    load_save.save_csv(df, season, 'scraped_data', file_name)

    return None



def reorganize_games_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorganize the games DataFrame so each game appears once with separate
    home/away team and score columns.

    :param df: Raw scraped games DataFrame
    :return: Cleaned games DataFrame with one row per game
    """

    # Remove leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # Remove the empty column that contains 'Limited ReportFull Report'
    if '' in df.columns:
        df = df.drop(columns=[''])

    # Clean the game strings
    df['Game'] = df['Game'].astype(str).str.strip()

    # Parse game info from strings like:
    # 2025-10-07 - Blackhawks 2, Panthers 3
    pattern = r'^(?P<Date>\d{4}-\d{2}-\d{2})\s*-\s*(?P<Away_Team>.+?)\s+(?P<Away_Score>\d+),\s*(?P<Home_Team>.+?)\s+(?P<Home_Score>\d+)$'

    extracted = df['Game'].str.extract(pattern)

    # Add parsed columns
    df['Date'] = extracted['Date']
    df['Away Team'] = extracted['Away_Team']
    df['Away Score'] = pd.to_numeric(extracted['Away_Score'])
    df['Home Team'] = extracted['Home_Team']
    df['Home Score'] = pd.to_numeric(extracted['Home_Score'])

    # Fix shortened names in parsed game columns
    df['Away Team'] = df['Away Team'].replace(constants.GAME_TEAM_NAME_FIXES)
    df['Home Team'] = df['Home Team'].replace(constants.GAME_TEAM_NAME_FIXES)

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Coyotes name correction for seasons before 2014-2015
    mask = df['Date'] < pd.Timestamp('2014-09-01')
    df.loc[mask & (df['Away Team'] == 'Arizona Coyotes'), 'Away Team'] = 'Phoenix Coyotes'
    df.loc[mask & (df['Home Team'] == 'Arizona Coyotes'), 'Home Team'] = 'Phoenix Coyotes'

    # Keep only one row per game
    df = df.drop_duplicates(subset=['Game']).copy()

    # Drop the original Game column
    df = df.drop(columns=['Game', 'Team'])

    # Reorder columns so game info comes first
    first_cols = ['Date', 'Away Team', 'Away Score', 'Home Team', 'Home Score']
    remaining_cols = [col for col in df.columns if col not in first_cols]
    df = df[first_cols + remaining_cols]

    return df


def scrape_games_data(season: str) -> None:
    """
    Scrape game results data for a given season and save the results as a CSV.

    :param season: Season string ('YYYY-YYYY')
    :return: None
    """

    url_season = season.replace("-", "")
    url = f'https://www.naturalstattrick.com/games.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&loc=B&team=All&rate=n'

    df = scrape_data(url)

    # Fix inconsistent team names in team column
    df = fix_team_names(df, ["Team"])

    # Reorganize so each game appears once
    df = reorganize_games_data(df)

    # Save as a CSV
    file_name = f'{season}_games.csv'
    load_save.save_csv(df, season, 'scraped_data', file_name)

    return None
