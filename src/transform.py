import logging
import pandas as pd

# Get logger
logger = logging.getLogger(__name__)


def process_standings_data(api_data, matches_data):
    logger.info("Processing standings data")

    standings = api_data['standings'][0]['table']
    form_map = build_team_form_map(matches_data)

    data_list = []

    for team_info in standings:
        team_id = team_info['team']['id']

        form = form_map.get(team_id, None)

        data_list.append([
            team_info['position'],
            team_info['team']['name'],
            team_info['playedGames'],
            team_info['won'],
            team_info['draw'],
            team_info['lost'],
            team_info['goalsFor'],
            team_info['goalsAgainst'],
            team_info['goalDifference'],
            team_info['points'],
            form
        ])

    columns = ['P','Team','GP','W','D','L','F','A','GD','Pts','Form']

    return pd.DataFrame(data_list, columns=columns)

'''
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
'''

def display_standings(df):
    """
    Display the standings DataFrame in the console.

    Args:
        df (pd.DataFrame): Standings DataFrame to display
    """
    print(df.to_string(index=False))

def compute_form(matches_data, team_id):
    """
    Convert match results into form string (e.g., WWDLW)
    """
    if not matches_data:
        return None

    form = []

    for match in matches_data.get("matches", []):
        home_id = match['homeTeam']['id']
        #away_id = match['awayTeam']['id']
        score = match['score']['fullTime']

        if score['home'] > score['away']:
            result = 'W' if home_id == team_id else 'L'
        elif score['home'] < score['away']:
            result = 'L' if home_id == team_id else 'W'
        else:
            result = 'D'

        form.append(result)

    return "".join(form)

def build_team_form_map(matches_data):
    """
    Returns: {team_id: "WWDLW"}
    """
    
    if not matches_data:
        return {}

    form_map = {}

    for match in matches_data.get("matches", []):
        home = match["homeTeam"]["id"]
        away = match["awayTeam"]["id"]
        score = match["score"]["fullTime"]

        if score["home"] is None:
            continue

        if score["home"] > score["away"]:
            winner = home
            loser = away
        elif score["home"] < score["away"]:
            winner = away
            loser = home
        else:
            winner = loser = None

        for team_id in [home, away]:
            if team_id not in form_map:
                form_map[team_id] = []

        if winner:
            form_map[winner].append("W")
            form_map[loser].append("L")
        else:
            form_map[home].append("D")
            form_map[away].append("D")

    # keep last 5 only
    return {
        team: "".join(results[-5:])
        for team, results in form_map.items()
    }
