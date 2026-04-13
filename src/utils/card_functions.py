# ====================================================================================================
# FUNCTIONS FOR TEAM CARD CREATION
# ====================================================================================================

# Imports
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import io
import ast
import cairosvg
import inflect
from PIL import Image, ImageDraw, ImageFont
from utils import card_helpers as ch
from utils import constants as constants
from utils import load_save as load_save


DATA_DIR = constants.DATA_DIR

# Load and cache fonts
BASIC_FONT_PATH = f'{DATA_DIR}/assets/fonts/basic.ttf'
HEADING_FONT_PATH = f'{DATA_DIR}/assets/fonts/header.ttf'

FONT_CACHE = {
    'basic_40': ImageFont.truetype(BASIC_FONT_PATH, 40),
    'basic_50': ImageFont.truetype(BASIC_FONT_PATH, 50),
    'basic_73': ImageFont.truetype(BASIC_FONT_PATH, 73),
    'basic_150': ImageFont.truetype(BASIC_FONT_PATH, 150),
    'heading_70': ImageFont.truetype(HEADING_FONT_PATH, 70),
    'heading_116': ImageFont.truetype(HEADING_FONT_PATH, 116),
}


def make_header_section(team_row: pd.Series, mode: str = 'light') -> Image:
    """
    Creates the header section of a team card as a PIL Image. The header includes team standings, season, 
    team logo, and key stats.

    :param team_row: A Series containing team data
    :param mode: A str determining the style of card ('light' or 'dark')
    :return: An Image of the header section
    """

    # Get basic team information
    team_name = team_row['Team']
    team_abbrev = team_row['Team Abbreviation']
    season = team_row['Season']

    # Get color variables
    if mode == 'light':
        background_color = constants.WHITE
        text_color = constants.DARK
        secondary_team_color = constants.SECONDARY_COLORS.get(team_abbrev)
    else:
        background_color = constants.DARK
        text_color = constants.WHITE
        secondary_team_color = constants.WHITE
    primary_team_color = constants.PRIMARY_COLORS.get(team_abbrev)
    header_text_color = constants.WHITE
    header_shadow_color = constants.SECONDARY_COLORS.get(team_abbrev)
    
    
    # Get standings variables
    wins = team_row['W']
    losses = team_row['L']
    otl = team_row['OTL']
    record = f'{wins}-{losses}-{otl}'
    point_percent = str(format(team_row['Point %'], '.3f'))
    points = str(team_row['Points'])
    goal_diff = team_row['GF'] - team_row['GA']
    if goal_diff > 0:
        goal_diff_str = f'+{goal_diff}'
    else: 
        goal_diff_str = str(goal_diff)

    inflect_engine = inflect.engine()
    div_rank = inflect_engine.ordinal(int(team_row['Division Rank']))
    if season != '2020-2021':
        conf_rank = inflect_engine.ordinal(int(team_row['Conference Rank']))
    else:
        conf_rank = 'N/A'
    league_rank = inflect_engine.ordinal(int(team_row['League Rank']))

    # Get stats variables
    goals_for_percent = str(format(team_row['EV_GF%'], '.3f'))
    xgoals_for_percent = str(format(team_row['EV_xGF%'], '.3f'))
    shots_for_percent = str(format(team_row['EV_SF%'], '.3f'))
    corsi_for_percent = str(format(team_row['EV_CF%'], '.3f'))
    fenwick_for_percent = str(format(team_row['EV_FF%'], '.3f'))
    shooting_percentage = str(format(team_row['EV_SH%'], '.3f'))
    save_percentage = str(format(team_row['EV_SV%'], '.3f'))

    # Create header section card
    header_section_width = 2000
    header_section_height = 700
    header_section = Image.new("RGB", (header_section_width, header_section_height), color=background_color)

    # Create draw object
    draw = ImageDraw.Draw(header_section)
    
    # Get team logo
    with open(f'{DATA_DIR}/assets/team_logos/{team_abbrev}_{mode}.svg', 'rb') as f:
        svg_bytes = f.read()
    team_logo = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_bytes))).convert("RGBA")

    # Calculate proportional height, resize and paste
    logo_width = 750
    w_percent = logo_width / team_logo.width
    logo_height = int(team_logo.height * w_percent)
    team_logo = team_logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    header_section.paste(team_logo, (-25, 150), team_logo)

    # Load fonts
    basic_font = FONT_CACHE['basic_50']
    subheading_font = FONT_CACHE['heading_70']
    heading_font = FONT_CACHE['heading_116']

 
    # Draw team standings text
    ch.draw_centered_text(draw, text='Standings', font=subheading_font, y_position=190, x_center=1000, fill=text_color)

    ch.draw_righted_text(draw, text='Record:', font=basic_font, y_position=250, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='Points %:', font=basic_font, y_position=300, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='Points:', font=basic_font, y_position=350, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='Goal Differential:', font=basic_font, y_position=400, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='Division Rank:', font=basic_font, y_position=450, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='Conference Rank:', font=basic_font, y_position=500, x_right=975, fill=text_color)
    ch.draw_righted_text(draw, text='League Rank:', font=basic_font, y_position=550, x_right=975, fill=text_color)

    draw.text(xy=(1025, 250), text=record, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 300), text=point_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 350), text=points, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 400), text=goal_diff_str, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 450), text=div_rank, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 500), text=conf_rank, font=basic_font, fill=text_color)
    draw.text(xy=(1025, 550), text=league_rank, font=basic_font, fill=text_color)

    # Draw team stats text
    ch.draw_centered_text(draw, text='5v5 STATS', font=subheading_font, y_position=190, x_center=1667, fill=text_color)

    ch.draw_righted_text(draw, text='Goals For %:', font=basic_font, y_position=250, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='xGoals For %:', font=basic_font, y_position=300, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='Shots For %:', font=basic_font, y_position=350, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='Corsi For %:', font=basic_font, y_position=400, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='Fenwick For %:', font=basic_font, y_position=450, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='Shooting %:', font=basic_font, y_position=500, x_right=1642, fill=text_color)
    ch.draw_righted_text(draw, text='Save %:', font=basic_font, y_position=550, x_right=1642, fill=text_color)

    draw.text(xy=(1692, 250), text=goals_for_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 300), text=xgoals_for_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 350), text=shots_for_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 400), text=corsi_for_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 450), text=fenwick_for_percent, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 500), text=shooting_percentage, font=basic_font, fill=text_color)
    draw.text(xy=(1692, 550), text=save_percentage, font=basic_font, fill=text_color)

    # Draw banner
    draw.polygon([(20, 20), (1980, 20), (1940, 140), (60, 140)], fill=primary_team_color)
    # Draw team name and season drop shadow
    draw.text(xy=(76, 28), text=team_name, font=heading_font, fill=header_shadow_color)
    ch.draw_righted_text(draw, season, heading_font, 28, 1920, fill=header_shadow_color)
    # Draw team name and season text
    draw.text(xy=(80, 24), text=team_name, font=heading_font, fill=header_text_color)
    ch.draw_righted_text(draw, season, heading_font, 24, 1924, fill=header_text_color)

    # Draw divider rectangles
    draw.rectangle([(664, 200), (669, 600)], fill=secondary_team_color)
    draw.rectangle([(1331, 200), (1336, 600)], fill=secondary_team_color)

    # Draw bottom rectangle
    draw.rectangle([(60, 660), (1940, 700)], fill=primary_team_color)

    return header_section


def make_rank_component(team_row: pd.Series, attribute_rank_name: str, mode: str = 'light') -> Image:
    """
    Creates a ranking component for a specific team attribute, displaying the team's rank, total teams, 
    percentile, and a visual percentile bar.

    :param team_row: A Series containing team data
    :param attribute_rank_name: A str representing the name of the attribute that is being ranked (e.g. 'gf_rank')
    :param mode: A str determining the style of card ('light' or 'dark')
    :return: An Image of the rank component
    """

    season = team_row['Season']

    # Get attribute name
    attribute_name = constants.ATTRIBUTE_NAMES.get(attribute_rank_name)

    # Get color variables
    if mode == 'light':
        background_color = constants.WHITE
        text_color = constants.DARK
        attribute_color = constants.DARK
    else:
        background_color = constants.DARK
        text_color = constants.WHITE
        attribute_color = constants.WHITE

    # Create ranking component card
    ranking_section_width = 300
    ranking_section_height = 240
    ranking_section = Image.new("RGB", (ranking_section_width, ranking_section_height), color=background_color)

    # Create draw object 
    draw = ImageDraw.Draw(ranking_section)
    
    # Get total teams
    total_teams = constants.SEASON_TEAM_NUM.get(season)

    # Get rank and percentile
    rank = int(team_row[attribute_rank_name])
    percentile = int(round((total_teams - rank) / (total_teams - 1), 2) * 100)

    # Get percentile color
    percentile_color = ch.get_percentile_color(percentile)
    
    # Get percentile bar variables
    bar_x, bar_y = 210, 82
    bar_width, bar_height = 78, 150
    border = 2

    height = percentile * 1.5

    percent_left = bar_x
    percent_right = bar_x + bar_width
    percent_bottom = bar_y + bar_height
    percent_top = percent_bottom - height

    # Draw the percentile bar
    draw.rectangle([bar_x - border, bar_y - border, bar_x + bar_width + border, bar_y + bar_height + border], 
                   fill=constants.GRAY, outline=text_color, width=border)
    draw.rectangle([percent_left, percent_top, percent_right, percent_bottom], fill=percentile_color)

    # Load fonts
    attribute_name_font = FONT_CACHE['basic_73']
    rank_font = FONT_CACHE['basic_150']
    total_teams_font = FONT_CACHE['basic_40']
    percentile_font = FONT_CACHE['basic_73']

    # Draw attribute name, rank, total teams, and percentile texts
    ch.draw_centered_text(draw, attribute_name, attribute_name_font, fill=attribute_color, y_position=-13, x_center=150)
    ch.draw_centered_text(draw, str(rank), rank_font, y_position=50, x_center=110, fill=text_color)
    ch.draw_centered_text(draw, f'/ {total_teams}', total_teams_font, y_position=200, x_center=110, fill=text_color)
    ch.draw_centered_text(draw, str(percentile), percentile_font, y_position=155, x_center=249, fill=text_color)
    
    # Draw rectangle
    draw.rectangle([(10, 64), (290, 70)], fill=attribute_color)
    
    return ranking_section


def make_elo_graph_section(team_row: pd.Series, mode: str = 'light') -> Image:
    """
    Creates a graph section displaying a team's Elo rating throughout the season.

    :param team_row: A Series containing team card data
    :param mode: 'light' or 'dark'
    :return: Image containing the Elo graph
    """

    season = team_row["Season"]

    # Convert Elo history string to list
    elo_history = ast.literal_eval(team_row["Elo History"])

    # X axis = games played
    games = list(range(len(elo_history)))

    # Season length
    season_games = constants.SEASON_GAMES.get(season)

    # Colors
    if mode == 'light':
        background_color = constants.WHITE
        text_color = constants.DARK
        graph_background_color = constants.GRAPH_WHITE
        graph_text_color = constants.GRAPH_DARK
    else:
        background_color = constants.DARK
        text_color = constants.WHITE
        graph_background_color = constants.GRAPH_DARK
        graph_text_color = constants.GRAPH_WHITE
    graph_blue = constants.GRAPH_BLUE


    # Section size
    graph_width = 950
    graph_height = 650
    graph_section = Image.new("RGB", (graph_width, graph_height), color=background_color)

    # Create matplotlib figure
    plt.style.use("default")
    fig, ax = plt.subplots(
        figsize=(graph_width / 200, (graph_height - 50) / 200),
        facecolor=graph_background_color,
        dpi=200
    )

    # Plot Elo
    ax.plot(
        games,
        elo_history,
        linewidth=2,
        color=graph_blue,
        marker="None",
        alpha=1
    )

    # X axis
    x_vals = [0, int(season_games * 0.25), int(season_games * 0.5), int(season_games * 0.75), int(season_games)]
    x_padding = 2
    ax.set_xlim(-x_padding, season_games + x_padding)
    ax.set_xticks(x_vals)
    ax.set_xticklabels(x_vals, fontsize=9, fontweight="bold")
    ax.tick_params(axis="x", labelsize=9, length=0, colors=graph_text_color)

    # Y axis
    y_ticks = [1300, 1400, 1500, 1600, 1700]
    y_padding = (1700 - 1300) * 0.10
    ax.set_ylim(1300 - y_padding, 1700 + y_padding)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks, fontsize=12, fontweight='bold', color=constants.GRAPH_GRAY)
    ax.tick_params(axis="y", labelsize=12, colors=constants.GRAPH_GRAY, length=0, pad=1)

    # Grid
    ax.grid(axis="y", linestyle="-", linewidth=2, color=constants.GRAPH_GRAY)
    ax.grid(axis="x", visible=False)
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)
    ax.set_facecolor(graph_background_color)

    plt.tight_layout()

    # Convert to image
    graph_img = ch.plot_to_image(fig)
    graph_img = graph_img.resize((graph_width, graph_height - 50))
    graph_section.paste(graph_img, (0, 30))

    # Load fonts
    subheading_font = FONT_CACHE['heading_70']

    # Create draw object
    draw = ImageDraw.Draw(graph_section)

    # Draw Elo graph title text
    ch.draw_centered_text(draw, text='Elo Rating Per Game', font=subheading_font, y_position=0, x_center=476, fill=text_color)

    plt.close(fig)

    return graph_section


def make_srs_graph_section(team_row: pd.Series, mode: str = 'light') -> Image:
    """
    Creates a graph section displaying a team's SRS rank history over the past 5 seasons.

    :param team_row: A Series containing team data including 'SRS Rank History' and 'Season'
    :param mode: 'light' or 'dark'
    :return: Image containing the SRS graph
    """

    # Parse SRS history
    srs_history = ast.literal_eval(team_row.get('SRS Rank History', '[]'))
    srs_history = srs_history[-5:]  # last 5 seasons

    # Get seasons (assumes current season is the last in data)
    cur_season = team_row["Season"]
    seasons = [cur_season]
    for _ in range(len(srs_history) - 1):
        seasons.append(load_save.get_prev_season(seasons[-1]))
    seasons.reverse()

    # Colors
    if mode == 'light':
        background_color = constants.WHITE
        text_color = constants.DARK
        graph_background_color = constants.GRAPH_WHITE
        graph_text_color = constants.GRAPH_DARK
    else:
        background_color = constants.DARK
        text_color = constants.WHITE
        graph_background_color = constants.GRAPH_DARK
        graph_text_color = constants.GRAPH_WHITE
    graph_red = constants.GRAPH_RED


    # Section size
    graph_width = 950
    graph_height = 650
    graph_section = Image.new("RGB", (graph_width, graph_height), color=background_color)

    # X positions (fixed)
    x_vals = list(range(1, len(srs_history) * 3 + 1, 3))

    # Y-axis range
    max_rank = constants.SEASON_TEAM_NUM.get(cur_season, 32)

    # Create matplotlib figure
    plt.style.use("default")
    fig, ax = plt.subplots(
        figsize=(graph_width / 200, (graph_height - 50) / 200),
        facecolor=graph_background_color,
        dpi=200
    )

    # Plot SRS ranks
    y_vals = srs_history
    ax.plot(x_vals, y_vals, marker="o", markersize=8, linewidth=3, color=graph_red, alpha=1)

    # X-axis
    ax.set_xticks(x_vals)
    ax.set_xticklabels(seasons, fontsize=9, fontweight="bold")
    ax.tick_params(axis="x", labelsize=9, length=0, colors=graph_text_color)
    ax.set_xlim(min(x_vals) - 1, max(x_vals) + 1)

    # Y-axis
    yticks = [1, 8, 16, math.ceil(max_rank * 0.75), max_rank]
    y_padding = (max_rank - 1) * 0.10
    ax.set_ylim(1 - y_padding, max_rank + y_padding)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=12, fontweight='bold', color=constants.GRAPH_GRAY)
    ax.tick_params(axis="y", labelsize=12, labelcolor=constants.GRAPH_GRAY, length=0, pad=1)
    ax.invert_yaxis()

    # Grid & styling
    ax.grid(axis="y", linestyle="-", linewidth=2, color=constants.GRAPH_GRAY)
    ax.grid(axis="x", visible=False)
    ax.spines[['top', 'bottom', 'left', 'right']].set_visible(False)
    ax.set_facecolor(graph_background_color)

    plt.tight_layout()

    # Convert to image
    graph_img = ch.plot_to_image(fig)
    graph_img = graph_img.resize((graph_width, graph_height - 50))
    graph_section.paste(graph_img, (0, 30))

    # Load fonts
    subheading_font = FONT_CACHE['heading_70']

    # Create draw object
    draw = ImageDraw.Draw(graph_section)

    # Draw SRS graph title text
    ch.draw_centered_text(draw, text='SRS Ranking Per Season', font=subheading_font, y_position=0, x_center=476, fill=text_color)

    plt.close(fig)

    return graph_section


def make_branding_section(team_abbrev: str, mode: str = 'light') -> Image:
    """
    Creates the branding section Image for the team card. The branding section contains references to my website and socials, references to data sources,
    and and is stylized using the specified team's colors.

    :param team_abbrev: A str representing the team abbreviation for the team to base the design color (e.g. 'TOR')
    :param mode: A str determining the style of card ('light' or 'dark')
    :return: An Image of branding section
    """

    # Get color variables
    if mode == 'light':
        background_color = constants.WHITE
        text_color = constants.DARK
        dividers_color = constants.SECONDARY_COLORS.get(team_abbrev)
    else:
        background_color = constants.DARK
        text_color = constants.WHITE
        dividers_color = constants.WHITE
    primary_team_color = constants.PRIMARY_COLORS.get(team_abbrev)
    header_text_color = constants.WHITE
    header_shadow_color = constants.SECONDARY_COLORS.get(team_abbrev)

    # Get updated date string
    update_date = constants.UPDATE_DATE

    # Create branding section card
    branding_section_width = 2000
    branding_section_height = 400
    branding_section = Image.new("RGB", (branding_section_width, branding_section_height), color=background_color)

    # Create draw image
    draw = ImageDraw.Draw(branding_section)

    # Get the font
    basic_font = FONT_CACHE['basic_73']
    
    # Branding text
    draw.text(xy=(100, 73), text='Website:', font=basic_font, fill=text_color)
    draw.text(xy=(100, 156), text='Socials:', font=basic_font, fill=text_color)

    ch.draw_righted_text(draw, 'analyticswithavery.com', basic_font, 73, 940, fill=text_color)
    ch.draw_righted_text(draw, 'analyticswavery', basic_font, 156, 940, fill=text_color)

    # Resources text
    draw.text(xy=(1060, 73), text='Team Data From:', font=basic_font, fill=text_color)
    draw.text(xy=(1060, 156), text='Date Updated:', font=basic_font, fill=text_color)

    ch.draw_righted_text(draw, 'naturalstattrick.com', basic_font, 73, 1900, fill=text_color)
    ch.draw_righted_text(draw, update_date, basic_font, 156, 1900, fill=text_color)  #'PuckPedia.com'
    
    # Get font
    heading_font = FONT_CACHE['heading_116']

    # Draw rectangles
    draw.rectangle([(60, 0), (1940, 40)], fill=primary_team_color)
    draw.rectangle([(998, 80), (1002, 220)], fill=dividers_color)

    # Draw branding shape
    draw.polygon([(60, 260), (1940, 260), (1980, 380), (20, 380)], fill=primary_team_color)
    ch.draw_centered_text(draw, 'Analytics With Avery', font=heading_font, y_position=268, x_center=996, fill=header_shadow_color)
    ch.draw_centered_text(draw, 'Analytics With Avery', font=heading_font, y_position=264, x_center=1000, fill=header_text_color)

    return branding_section


def make_team_card(team: str, season: str, mode: str ='light', save: bool=True,) -> Image:
    """
    Create a full team card image for a given team and season.

    :param team: Full team name
    :param season: Season string ('YYYY-YYYY')
    :param mode: Card style ('light' or 'dark')
    :param save: Whether to save the generated card as a PNG
    :return: PIL Image containing the completed team card
    """

    # Get the team's card data for the given season
    team_season_data = load_save.load_card_data(season)
    team_row = team_season_data[team_season_data["Team"] == team].iloc[0]

    team_abbrev = team_row['Team Abbreviation']

    # Get color variables
    if mode == 'light':
        background_color = constants.WHITE
        secondary_team_color = constants.SECONDARY_COLORS.get(team_abbrev)
    else:
        background_color = constants.DARK
        secondary_team_color = constants.WHITE
    primary_team_color = constants.PRIMARY_COLORS.get(team_abbrev)

    # Create team card
    card_width = 2000
    card_height = 2400
    team_card = Image.new('RGB', (card_width, card_height), color=background_color)

    draw = ImageDraw.Draw(team_card)

    # Add header section
    header_section = make_header_section(team_row, mode)
    team_card.paste(header_section, (0, 0))

    # Add Elo graph section
    elo_graph = make_elo_graph_section(team_row, mode)
    team_card.paste(elo_graph, (50, 720))

    # Add SRS graph section
    srs_graph = make_srs_graph_section(team_row, mode)
    team_card.paste(srs_graph, (1000, 720))

    # Draw graph divider rectangle
    draw.rectangle([(998, 740), (1002, 1240)], fill=secondary_team_color)

    # Draw divider rectangle
    draw.rectangle([(60, 1340), (1940, 1380)], fill=primary_team_color)

    # Add ranking sections
    xgf_rank_section = make_rank_component(team_row, 'xgf_rank', mode)
    team_card.paste(xgf_rank_section, (50, 1425))

    xga_rank_section = make_rank_component(team_row, 'xga_rank', mode)
    team_card.paste(xga_rank_section, (50, 1715))

    gf_rank_section = make_rank_component(team_row, 'gf_rank', mode)
    team_card.paste(gf_rank_section, (455, 1425))

    ga_rank_section = make_rank_component(team_row, 'ga_rank', mode)
    team_card.paste(ga_rank_section, (455, 1715))

    pp_rank_section = make_rank_component(team_row, 'pp_rank', mode)
    team_card.paste(pp_rank_section, (850, 1425))

    pk_rank_section = make_rank_component(team_row, 'pk_rank', mode)
    team_card.paste(pk_rank_section, (850, 1715))

    sf_rank_section = make_rank_component(team_row, 'sf_rank', mode)
    team_card.paste(sf_rank_section, (1245, 1425))

    sa_rank_section = make_rank_component(team_row, 'sa_rank', mode)
    team_card.paste(sa_rank_section, (1245, 1715))

    fn_rank_section = make_rank_component(team_row, 'fn_rank', mode)
    team_card.paste(fn_rank_section, (1640, 1425))

    gt_rank_section = make_rank_component(team_row, 'gt_rank', mode)
    team_card.paste(gt_rank_section, (1640, 1715))

    # Add branding section
    branding_section = make_branding_section(team_abbrev, mode)
    team_card.paste(branding_section, (0, 2000))

    # Save team card
    team_card = team_card.convert('RGB')
    file_name = f"{season}_{team_abbrev}_{mode}.png"
    if save:
        load_save.save_card(team_card, season, file_name)

    print(f'========== {team} card ({mode}) created for the {season} season! ==========')

    return team_card
