"""
Transform Module

This module handles data transformation and processing.
"""

import logging
import pandas as pd
from streamlit import table

# Get logger
logger = logging.getLogger(__name__)


def process_standings_data(api_data):
    """
    Process raw API data into a clean pandas DataFrame.

    Args:
        api_data (dict): Raw JSON data from the API

    Returns:
        pd.DataFrame: Processed standings data
    """
    logger.info("Processing standings data")

    # Extract the standings table from the API response
    standings = api_data['standings'][0]['table']

    # Initialize list to store processed team data
    data_list = []

    # Loop through each team in the standings and extract relevant statistics 
    for team_info in standings:
        rank = team_info['position']
        team_name = team_info['team']['name']
        played = team_info['playedGames']
        win = team_info['won']
        draw = team_info['draw']
        lose = team_info['lost']
        goals_for = team_info['goalsFor']
        goals_against = team_info['goalsAgainst']
        goals_diff = team_info['goalDifference']
        points = team_info['points']

        # Append team data as a list to data_list
        data_list.append([rank, team_name, played, win, draw, lose, goals_for, goals_against, goals_diff, points])

    # Create pandas DataFrame from the collected data
    columns = ['P', 'Team', 'GP', 'W', 'D', 'L', 'F', 'A', 'GD', 'Pts']
    standings_df = pd.DataFrame(data_list, columns=columns)

    logger.info(f"Processed {len(standings_df)} teams' data")
    return standings_df


def display_standings(df):
    """
    Display the standings DataFrame in the console.

    Args:
        df (pd.DataFrame): Standings DataFrame to display
    """
    print(df.to_string(index=False))