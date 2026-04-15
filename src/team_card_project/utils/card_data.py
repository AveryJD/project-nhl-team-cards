# ====================================================================================================
# FUNCTIONS FOR GETTING ALL DATA USED IN TEAM CARDS
# ====================================================================================================

# Imports
import pandas as pd
from team_card_project.utils import constants
from team_card_project.utils import load_save


def make_league_rankings(all_df: pd.DataFrame, season: str) -> pd.DataFrame:
    """
    Create league, conference, and division rankings using NHL tiebreakers.

    :param all_df: DataFrame containing team season stats in all situations
    :param season: season string ('YYYY-YYYY')
    :return: DataFrame with team rankings
    """

    df = all_df.copy()

    # Add conference + division
    team_map = constants.TEAM_DIVISION_BY_SEASON[season]


    df["Division"] = df["Team"].map(team_map)
    df["Conference"] = df["Division"].map(constants.DIVISION_CONFERENCE)

    # Sort using NHL tiebreakers
    df = df.sort_values(
        by=[
            "Points",                   # Total points
            "Point %",                  # Fewer GP
            "Regulation Wins",          # Regulation wins 
            "Regulation/Overtime Wins", # Regulation and overtime wins
            "Wins",                     # Total wins
            "Goal Differential",        # Goal differential
            "Goals For"                 # Goals for
        ],
        ascending=[False, False, False, False, False, False, False]
    ).reset_index(drop=True)

    # League rank
    df["League Rank"] = df.index + 1

    # Conference rank
    if season == "2020-2021":
        df["Conference Rank"] = "N/A"
    else:
        df["Conference Rank"] = (
            df.groupby("Conference")
            .cumcount() + 1
        )

    # Division rank
    df["Division Rank"] = (
        df.groupby("Division")
        .cumcount() + 1
    )

    rankings_df = df[[
        "Team",
        "League Rank",
        "Conference Rank",
        "Division Rank"
    ]]

    return rankings_df


def make_attribute_rankings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add league-wide rankings for key team card attributes.

    :param df: DataFrame containing team card statistics
    :return: DataFrame with added ranking columns
    """

    rank_map = {
        "gf_rank": ("EV_GF", False),
        "ga_rank": ("EV_GA", True),
        "xgf_rank": ("EV_xGF", False),
        "xga_rank": ("EV_xGA", True),
        "pp_rank": ("PP_GF", False),
        "pk_rank": ("PK_GA", True),
        "sf_rank": ("SF", False),
        "sa_rank": ("SA", True),
        "fn_rank": ("GAx", False),
        "gt_rank": ("GSAx", False),
    }

    # stats that should be converted to per-game rates
    per_game_stats = {
        "EV_GF", "EV_GA", "EV_xGF", "EV_xGA",
        "PP_GF", "PK_GA",
        "SF", "SA",
        "GAx", "GSAx"
    }

    for rank_col, (stat_col, ascending) in rank_map.items():

        if stat_col in per_game_stats:
            stat_series = df[stat_col] / df["Games Played"]
        else:
            stat_series = df[stat_col]

        df[rank_col] = (
            stat_series
            .rank(ascending=ascending, method="min")
            .astype(int)
        )

    return df


def make_card_data(season: str) -> None:
    """
    Generate a CSV file of all the relevant team card data from other CSV files
    
    :param season: A str of the season to make the card data for ('YYYY-YYYY')
    :return: None
    """

    # Load team data
    all_df = load_save.load_team_data(season, 'all')
    ev_df = load_save.load_team_data(season, '5v5')
    pp_df = load_save.load_team_data(season, '5v4')
    pk_df = load_save.load_team_data(season, '4v5')

    standings_df = load_save.load_standings(season)

    # Initialize dictionary with empty lists for all teams
    srs_rows = {team_name: [] for team_name in constants.TEAM_NAMES.values()}

    # Collect 5 seasons of SRS ratings
    cur_season = season
    for _ in range(5):
        try:
            all_srs_df = load_save.load_srs(cur_season)
            for team_full_name in constants.TEAM_NAMES.values():
                if team_full_name == "Arizona Coyotes" and cur_season <= "2013-2014":
                    row = all_srs_df[all_srs_df["Team"] == "Phoenix Coyotes"]
                else:
                    row = all_srs_df[all_srs_df["Team"] == team_full_name]

                if not row.empty:
                    srs_rows[team_full_name].insert(0, row.iloc[0]["SRS Rank"])
                else:
                    srs_rows[team_full_name].insert(0, None)
        except FileNotFoundError:
            for team_full_name in constants.TEAM_NAMES.values():
                srs_rows[team_full_name].insert(0, None)
        cur_season = load_save.get_prev_season(cur_season)

    # Convert to DataFrame
    srs_df = pd.DataFrame([
        {
        "Team": team_name, 
        "SRS Rank History": [float(r) if r is not None else None for r in ratings]
        }
        for team_name, ratings in srs_rows.items()
    ])

    # Load elo data
    elo_rows = []

    for team in constants.TEAM_NAMES:
        try:
            elo_df = load_save.load_elo(season, team)

            elo_rows.append({
                "Team": constants.TEAM_NAMES.get(team),
                "Elo History": elo_df["Elo"].tolist()
            })

        except FileNotFoundError:
            continue

    elo_df = pd.DataFrame(elo_rows)

    # Select important columns from each DataFrame
    standings_cols = standings_df[[
        'Team',
        'Games Played',
        'Wins',
        'Losses',
        'Overtime/Shootout Losses',
        'Regulation Wins',
        'Regulation/Overtime Wins',
        'Points',
        'Point %',
        'Goals For',
        'Goals Against',
        'Goal Differential'
    ]]

    all_cols = all_df[[
        'Team',
        'GF',
        'GA',
        'xGF',
        'xGA',
        'SF',
        'SA',
        'SV%'
    ]]

    base_cols = standings_cols.merge(all_cols, on='Team', how='left')

    ev_cols = (
        ev_df[['Team', 'GF', 'GA', 'xGF', 'xGA', 'GF%', 'xGF%', 'SF%', 'CF%', 'FF%', 'SH%', 'SV%']]
        .rename(columns=lambda c: f'EV_{c}' if c != 'Team' else c)
    )

    num_cols = ev_cols.select_dtypes(include='number').columns
    ev_cols[num_cols] = ev_cols[num_cols] / 100

    pp_cols = (
        pp_df[['Team', 'GF']]
        .rename(columns={
            'GF': 'PP_GF'
        })
    )

    pk_cols = (
        pk_df[['Team', 'GA']]
        .rename(columns={
            'GA': 'PK_GA'
        })
    )

    # Merge all data
    card_info_df = (
        base_cols
        .merge(ev_cols, on="Team", how="left")
        .merge(pp_cols, on="Team", how="left")
        .merge(pk_cols, on="Team", how="left")
        .merge(srs_df, on="Team", how="left")
        .merge(elo_df, on="Team", how="left")
    )

    # Add league rankings
    league_rankings = make_league_rankings(card_info_df, season)

    card_info_df = card_info_df.merge(
        league_rankings,
        on="Team",
        how="left"
    )

    # Add finishing and goaltending metrics
    card_info_df["GAx"] = card_info_df["GF"] - card_info_df["xGF"]
    card_info_df["GSAx"] = card_info_df["xGA"] - card_info_df["GA"]

    # Add season as first column
    card_info_df.insert(0, "Season", season)

    # Add a team abbreviation column
    team_to_abbrev = {v: k for k, v in constants.TEAM_NAMES.items()}
    card_info_df["Team Abbreviation"] = card_info_df["Team"].map(team_to_abbrev)
    cols = list(card_info_df.columns)
    cols.insert(2, cols.pop(cols.index("Team Abbreviation")))
    card_info_df = card_info_df[cols]

    # Add rankings
    card_info_df = make_attribute_rankings(card_info_df)

    # Sort
    card_info_df = card_info_df.sort_values("Points", ascending=False).reset_index(drop=True)

    # Save
    file_name = f"{season}_team_card_data.csv"
    load_save.save_card_data(card_info_df, file_name)
