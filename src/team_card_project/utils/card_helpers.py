# ====================================================================================================
# CARD CREATION HELPER FUNCTIONS
# ====================================================================================================

# Imports
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io
import os
from utils import constants
from utils import load_save


DATA_DIR = constants.DATA_DIR


def draw_centered_text(
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.ImageFont,
        y_position: int,
        x_center: int = 1000,
        fill: tuple[int, int, int] = (0, 0, 0)
    ) -> None:    
    """
    Draws text that is centered on a PIL drawing.

    :param draw: A PIL drawing that will have the text centered on it
    :param text: A str of the text to be centered
    :param font: An ImageFont of the text's font
    :param y_position: An int of where the y position will be
    :param x_center: An int of where the center x position is (default is at 1000)
    :param fill: A tuple of rgb values for the color of the text (default is (0,0,0)/black)
    :return: None
    """

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x_position = x_center - (text_width // 2)  
    draw.text((x_position, y_position), text, font=font, fill=fill)


def draw_righted_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    y_position: int,
    x_right: int,
    fill: tuple[int, int, int] = (0, 0, 0)
    ) -> None:
    """
    Draws text that right-aligned on a PIL drawing.

    :param draw: A PIL drawing that will have the text right-aligned on it
    :param text: A str of the text to be right-aligned
    :param font: An ImageFont of the text's font
    :param y_position: An int of where the y position will be
    :param x_right: An int of where the right most x position is
    :param fill: A tuple of rgb values for the color of the text (default is (0,0,0)/black)
    :return: None
    """

    text_width = draw.textbbox((0, 0), str(text), font=font)[2] 
    x_position = x_right - text_width 
    draw.text((x_position, y_position), str(text), font=font, fill=fill)


def plot_to_image(fig: plt.Figure) -> Image:
    """
    Change a matplotlib plot into a PIL image.

    :param fig: A Matplotlib plot to be turned into an image
    :return: A PIL image of the plot
    """

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=500)
    buf.seek(0)
    img = Image.open(buf)

    return img


def get_percentile_color(percentile: int) -> tuple[int, int, int]:
    """
    Return an RGB color based on the percentile rank.
    0%   -> Red (255, 0, 0)
    25%  -> Orange (255, 165, 0)
    50%  -> Yellow (255, 255, 0)
    75%  -> Light Green (144, 238, 144)
    100% -> Dark Green (0, 128, 0)

    :param percentile: An int of the percentile to return the color for
    :return: A tuple containing normalized RGB values that correspond to the given percentile
    """
    if percentile <= 25:
        # Get color between red (255,0,0) and orange (255,165,0)
        ratio = percentile / 25
        r = 255
        g = int(165 * ratio)
        b = 0
    elif percentile <= 50:
        # Get color between orange (255,165,0) and yellow (255,255,0)
        ratio = (percentile - 25) / 25
        r = 255
        g = 165 + int(90 * ratio)
        b = 0
    elif percentile <= 75:
        # Get color between yellow (255,255,0) and light green (144,238,144)
        ratio = (percentile - 50) / 25
        r = 255 - int((255 - 144) * ratio)
        g = 255 - int((255 - 238) * ratio)
        b = int(144 * ratio)
    else:
        # Get color between light green (144,238,144) and dark green (0,128,0)
        ratio = (percentile - 75) / 25
        r = 144 - int(144 * ratio)
        g = 238 - int((238 - 128) * ratio)
        b = 144 - int(144 * ratio)

    return (r, g, b)


def get_team_seasons_srs(team, cur_season, seasons_num: int = 5):
    """
    Get a team's SRS ratings from the current season and previous seasons.

    :param team: Team abbreviation or name
    :param cur_season: Current season string ('YYYY-YYYY')
    :param seasons_num: Number of seasons to collect
    :return: A list of SRS ratings across seasons
    """
    seasons_srs = []

    for _ in range(seasons_num):
        srs_file_path = os.path.join(DATA_DIR, "team_card_data", cur_season, "results", f"{cur_season}_srs.csv")

        srs_df = pd.read_csv(srs_file_path)

        team_srs = srs_df.loc[srs_df["Team"] == team, "SRS Rating"].iloc[0]
        if team == 'ARI' and team_srs is None:
            team = 'PHX'
            team_srs = srs_df.loc[srs_df["Team"] == team, "SRS Rating"].iloc[0]

        seasons_srs.append(team_srs)

        cur_season = load_save.get_prev_season(cur_season)

    return seasons_srs
