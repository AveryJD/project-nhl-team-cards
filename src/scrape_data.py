# ====================================================================================================
# FUNCTIONS FOR SCRAPING DATA FROM NATURALSTATTRICK
# ====================================================================================================

# Imports
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import time
import random
import constants


DATA_DIR = constants.DATA_DIR


def random_delay() -> None:
    """
    Introduce a random delay between web requests to reduce server load and avoid rate limiting.

    :return: None
    """
    # Make delay by a random time of 10-20 seconds
    delay = random.uniform(10, 20)
    print(f"Waiting {delay:.2f} seconds before next request")
    time.sleep(delay)


def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.

    :param url: The URL to fetch
    :return: The content of the fetched page, or None if the request fails
    """
    # Delay before fetching the page
    random_delay()

    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()

    return response.content


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


def scrape_standings_data(season: str) -> None:
    """
    
    """

    url_season = season.replace("-", "")
    url = f'https://www.naturalstattrick.com/teamtable.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td='

    df = scrape_data(url)

    df['Points'] = pd.to_numeric(df['Points'])
    df = df.sort_values(by='Points', ascending=False)

    df = df.drop(df.columns[0], axis=1)

    # Save as a CSV
    filename = f'{season}_standings_data.csv'
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, 'standings')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    df.to_csv(save_path, index=False)
    print(f"Saved {filename}")

    return None


def scrape_games_data(season: str) -> None:
    """
    
    """

    url_season = season.replace("-", "")
    url = f'https://www.naturalstattrick.com/games.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit=all&loc=B&team=All&rate=n'

    df = scrape_data(url)

    # Save as a CSV
    filename = f'{season}_game_data.csv'
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, 'games')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    df.to_csv(save_path, index=False)
    print(f"Saved {filename}")

    return None


def scrape_team_data(season: str, situation: str, team_abbreviation: str) -> None:
    """
    
    """

    special_team_map = constants.SPECIAL_TEAM_MAP 

    if team_abbreviation in ['LAK', 'NJD', 'SJS', 'TBL']:
        url_team = special_team_map.get(team_abbreviation)
    else:
        url_team = team_abbreviation

    url_season = season.replace("-", "")
    url = f'https://www.naturalstattrick.com/playerteams.php?fromseason={url_season}&thruseason={url_season}&stype=2&sit={situation}&score=all&stdoi=std&rate=n&team={url_team}&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL#'

    df = scrape_data(url)

    # Skip saving if DataFrame is empty
    if df.empty:
        print(f"No data for {team_abbreviation} in {season}")
        return None

    df['Total Points'] = pd.to_numeric(df['Total Points'])
    df = df.sort_values(by='Total Points', ascending=False)

    df = df.drop(df.columns[0], axis=1)

    # Save as a CSV
    filename = f'{season}_{situation}_{team_abbreviation}_team_data.csv'
    save_dir = os.path.join(DATA_DIR, 'team_card_data', season, f'teams_{situation}', )
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    df.to_csv(save_path, index=False)
    print(f"Saved {filename} to {save_dir}")

    return None



def main():
    """
    
    """

    for season in constants.SEASONS:

        #scrape_standings_data(season)
        
        #scrape_games_data(season)

        for situation in constants.SITUATIONS:
            for team_abbreviation in constants.TEAM_NAMES:
                scrape_team_data(season, situation, team_abbreviation)

    return None


if __name__ == "__main__":
    main()
